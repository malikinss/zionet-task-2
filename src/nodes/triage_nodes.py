# ./src/nodes/triage_nodes.py

"""OOP-style node container for the application processing pipeline.

This module provides `TriageNodes`, a class that bundles all pipeline
node methods together with a shared LLM client and logger, allowing
dependency injection and easier testing compared to module-level
node functions.

Example:
    Basic usage:
    ```
    from src.nodes.triage_nodes import TriageNodes
    from src.llm import GroqClient
    from src.logger import AppLogger

    nodes = TriageNodes(llm=GroqClient(), logger=AppLogger("triage"))
    graph.add_node("preprocess", nodes.preprocess)
    graph.add_node("classify", nodes.classify)
    ```
"""

from src.types import ApplicationState, ApplicationClassification
from src.llm import GroqClient
from src.logger import AppLogger
from src.prompts import CLASSIFIER_PROMPT


class TriageNodes:
    """A container for all pipeline node methods with shared dependencies.

    Bundles preprocessing, classification, routing, and terminal node
    methods into a single class, sharing one `GroqClient` and one
    `AppLogger` instance across all nodes.

    Attributes:
        _llm: `GroqClient` instance used for LLM calls in classify.
        _logger: `AppLogger` instance used for structured logging
            across all nodes.

    Example:
    ```
    nodes = TriageNodes(llm=GroqClient(), logger=AppLogger("triage"))
    graph.add_node("preprocess", nodes.preprocess)
    graph.add_node("classify", nodes.classify)
    graph.add_node("shortlist", nodes.shortlist)
    ```
    """

    def __init__(self, llm: GroqClient, logger: AppLogger):
        """Initializes `TriageNodes` with an LLM client and a logger.

        Args:
            llm: `GroqClient` instance used for classification calls.
            logger: `AppLogger` instance used across all node methods.

        Example:
        ```
        nodes = TriageNodes(
            llm=GroqClient(),
            logger=AppLogger("triage")
        )
        ```
        """
        self._llm = llm
        self._logger = logger

    def preprocess(self, state: ApplicationState) -> dict:
        """Cleans and normalizes raw application data.

        Reads `raw_input` from state and produces a cleaned dict with
        normalized name casing, lowercased email and skills, a parsed
        integer experience value, and stripped whitespace throughout.

        Args:
            state: The current application state with a populated
                `raw_input` field.

        Returns:
            A dict with a single key `"cleaned"` containing the
            normalized application data.

        Example:
        ```
        result = nodes.preprocess(state)
        print(result["cleaned"]["name"])   # "Jane Doe"
        print(result["cleaned"]["skills"]) # ["python", "sql"]
        ```
        """
        log = self._logger.node("[PREPROCESS]")
        log.start("Cleaning application data")
        raw = state["raw_input"]
        cleaned = {
            "name": raw.get("name", "").strip().title(),
            "email": raw.get("email", "").strip().lower(),
            "position": raw.get("position", "").strip(),
            "experience_years": int(raw.get("experience_years", 0)),
            "skills": [s.strip().lower() for s in raw.get("skills", [])],
            "cover_letter": raw.get("cover_letter", "").strip(),
        }
        log.done(f"{cleaned['name']} → {cleaned['position']}")
        return {"cleaned": cleaned}

    def classify(self, state: ApplicationState) -> dict:
        """Classifies a cleaned application using the LLM.

        Sends the cleaned application data to the LLM with
        `CLASSIFIER_PROMPT` as the system message, strips any markdown
        fences from the response, and parses it into an
        `ApplicationClassification`.

        Args:
            state: The current application state with a populated
                `cleaned` field.

        Returns:
            A dict with a single key `"classification"` containing
            the parsed ApplicationClassification instance.

        Example:
        ```
        result = nodes.classify(state)
        print(result["classification"].category)  # "shortlist"
        print(result["classification"].score)     # 87
        """
        log = self._logger.node("[CLASSIFY]")
        log.start("Analyzing application with LLM")
        cleaned = state["cleaned"]
        raw_json = self._llm.complete(
            system=CLASSIFIER_PROMPT,
            user=self._get_user_message(cleaned),
        )
        raw_json = self._extract_json(raw_json)
        classification = ApplicationClassification.model_validate_json(
            raw_json
        )
        log.done(f"{classification.category} (score={classification.score})")
        return {"classification": classification}

    def router(self, state: ApplicationState) -> str:
        """Reads the classification category and returns it as a routing key.

        Args:
            state: The current application state with a populated
                `classification` field.

        Returns:
            The category string from the classification: one of
            `"shortlist"`, `"reject"`, or `"escalate"`.

        Raises:
            ValueError: If classification is missing from state.

        Example:
        ```
        route = nodes.router(state)
        print(route)  # "shortlist"
        """
        log = self._logger.node("[ROUTER]")
        c = self._get_classification(state)
        log.info(f"Routing to: {c.category.upper()}")
        return c.category

    def shortlist(self, state: ApplicationState) -> dict:
        """Handles shortlisted applications by logging interview scheduling.

        Args:
            state: The current application state with populated
                `classification` and `cleaned` fields.

        Returns:
            A dict with `"decision"` set to `"shortlist"`.

        Raises:
            ValueError: If classification is missing from state.

        Example:
        ```
        result = nodes.shortlist(state)
        print(result["decision"])  # "shortlist"
        """
        log = self._logger.node("[SHORTLIST]")
        c = self._get_classification(state)
        log.start(f"Scheduling interview for: {state['cleaned']['name']}")
        log.info(f"Score: {c.score}/100 | Urgency: {c.urgency}")
        log.done(c.reasoning)
        return {"decision": "shortlist"}

    def reject(self, state: ApplicationState) -> dict:
        """
        Handles rejected applications with an interactive confirmation prompt.

        Prompts the user to confirm the rejection. If confirmed, records
        the decision as `"reject"`; otherwise escalates to human review.

        Args:
            state: The current application state with populated
                `classification` and `cleaned` fields.

        Returns:
            A dict with `"decision"` set to `"reject"` if the user
            confirms, or `"escalate"` if the user cancels.

        Raises:
            ValueError: If classification is missing from state.

        Example:
        ```
        # User types "yes":
        result = nodes.reject(state)
        print(result["decision"])  # "reject"

        # User types anything else:
        result = nodes.reject(state)
        print(result["decision"])  # "escalate"
        """
        log = self._logger.node("[REJECT]")
        c = self._get_classification(state)
        name = state["cleaned"]["name"]
        log.start(f"About to send rejection to: {name}")
        log.info(f"Score: {c.score}/100 | Reason: {c.reasoning}")
        log.human_input(
            "Send rejection letter? "
            "Type 'yes' to confirm, anything else to escalate"
        )
        answer = input("  >>> ").strip().lower()
        if answer == "yes":
            log.done(f"Rejection confirmed for: {name}")
            return {"decision": "reject"}
        else:
            self._logger.node("[ESCALATE]").info(
                "Rejection cancelled — escalating to human review"
            )
            return {"decision": "escalate"}

    def escalate(self, state: ApplicationState) -> dict:
        """Handles applications flagged for human review.

        Logs the candidate name, score, and missing information, then
        records the decision as `"escalate"`.

        Args:
            state: The current application state with populated
                `classification` and `cleaned` fields.

        Returns:
            A dict with `"decision"` set to `"escalate"`.

        Raises:
            ValueError: If classification is missing from state.

        Example:
        ```
        result = nodes.escalate(state)
        print(result["decision"])  # "escalate"
        """
        log = self._logger.node("[ESCALATE]")
        c = self._get_classification(state)
        log.start(f"Flagging for human review: {state['cleaned']['name']}")
        log.info(f"Score: {c.score}/100")
        log.done(f"Missing info: {c.missing_info}")
        return {"decision": "escalate"}

    def _get_classification(
        self, state: ApplicationState
    ) -> ApplicationClassification:
        """Retrieves the classification from state, raising if absent.

        Args:
            state: The current application state.

        Returns:
            The `ApplicationClassification` stored in state.

        Raises:
            ValueError: If `state["classification"]` is None.

        Example:
        ```
        c = self._get_classification(state)
        print(c.category)  # "shortlist"
        """
        c = state["classification"]
        if c is None:
            raise ValueError("Classification is missing from state")
        return c

    def _extract_json(self, raw: str, language: str = "json") -> str:
        """Strips markdown code fence wrappers from a string.

        Args:
            raw: Raw string that may be wrapped in a markdown code fence.
            language: Language tag following the opening fence. Defaults
                to `"json"`.

        Returns:
            The unwrapped and stripped content string.

        Example:
        ```
        self._extract_json("```json\\n{...}\\n```")  # "{...}"
        self._extract_json("{...}")                   # "{...}"
        """
        fence = "```"
        return (
            raw.strip()
            .removeprefix(f"{fence}{language}")
            .removeprefix(fence)
            .removesuffix(fence)
            .strip()
        )

    def _get_user_message(self, data: dict) -> str:
        """
        Formats cleaned application data into a user message string for
        the LLM.

        Args:
            data: Cleaned application dict with keys `position`, `name`,
                `experience_years`, `skills`, and `cover_letter`.

        Returns:
            A formatted multi-line string summarizing the application.

        Example:
        ```
        self._get_user_message({
            "position": "Engineer",
            "name": "Jane Doe",
            "experience_years": 5,
            "skills": ["python", "sql"],
            "cover_letter": "I am excited to apply."
        })
        # "Position: Engineer\\nCandidate: Jane Doe\\n..."
        """
        return (
            f"Position: {data['position']}\n"
            f"Candidate: {data['name']}\n"
            f"Experience: {data['experience_years']} years\n"
            f"Skills: {', '.join(data['skills'])}\n"
            f"Cover Letter: {data['cover_letter']}\n"
        )
