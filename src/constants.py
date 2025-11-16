"""Constants used across the project."""

from llm_cgr import OptionsEnum


class HallucinationLevel(OptionsEnum):
    """Enum for the different levels of hallucinations to be tested."""

    LIBRARY = "library"
    MEMBER = "member"

    def lil(self) -> str:
        """Return a short string representation of the enum value."""
        return self.value[:3].lower()


# the default model parameters for the experiments
MODEL_DEFAULTS: dict[str, dict[str, float | None]] = {
    "gpt-4o-mini-2024-07-18": {
        "temperature": 1.0,
        "top_p": 1.0,
    },
    "gpt-5-mini-2025-08-07": {
        "temperature": 1.0,
        "top_p": 1.0,
    },
    "ministral-8b-2410": {
        "temperature": 0.3,
        "top_p": 1.0,
    },
    "qwen/qwen2.5-coder-32b-instruct": {
        "temperature": 0.7,
        "top_p": 0.8,
    },
    "meta-llama/llama-3.3-70b-instruct-turbo": {
        "temperature": 0.6,
        "top_p": 0.9,
    },
    "deepseek-chat": {  # deepseek-v3.1 (non-thinking mode)
        "temperature": 0.6,
        "top_p": 0.5,
    },
    "claude-haiku-4-5-20251001": {
        "temperature": 1.0,
        "top_p": None,  # defaults to 1.0, api does not allow configuration of both
    },
    # our finetuned versions of ministral-8b
    "ft:ministral-8b-latest:7da9de33:20251113:d36adf52": {  # 5 epochs, 0.0001 lr
        "temperature": 0.3,
        "top_p": 1.0,
    },
    "ft:ministral-8b-latest:7da9de33:20251114:90da8eec": {  # 10 epochs, 0.0001 lr
        "temperature": 0.3,
        "top_p": 1.0,
    },
    "ft:ministral-8b-latest:7da9de33:20251115:6eb2304d": {  # 5 epochs, 0.00001 lr
        "temperature": 0.3,
        "top_p": 1.0,
    },
    "ft:ministral-8b-latest:7da9de33:20251115:993ca18f": {  # 10 epochs, 0.00001 lr
        "temperature": 0.3,
        "top_p": 1.0,
    },
}


# the libraries used in the study, they are both:
#   - documented online
#   - used in BigCodeBench
# fmt: off
DOCUMENTED_LIBRARIES = [
    'bs4', 'chardet', 'cryptography', 'dateutil', 'django',
    'folium', 'librosa', 'lxml', 'matplotlib', 'nltk',
    'numpy', 'openpyxl', 'pandas', 'psutil', 'pytesseract',
    'pytz', 'regex', 'requests', 'scipy', 'seaborn',
    'sklearn', 'statsmodels', 'sympy', 'tensorflow', 'textblob',
    'texttable', 'wordcloud', 'wordninja', 'xlwt', 'xmltodict',
]
# fmt: on
