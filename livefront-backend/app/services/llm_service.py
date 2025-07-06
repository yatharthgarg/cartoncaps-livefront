import logging
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from ..config import settings

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        model_name = settings.LLM_MODEL
        logger.info(f"Initializing LLMService with model: {model_name}")

        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()

        logger.info(f"Loaded model on device: {self.device}")

    def generate(self, prompt: str) -> str:
        """
        Asynchronously generate a completion for the given prompt.
        Returns the full generated text (with prompt echo stripped).
        """
        try:
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=settings.MAX_INPUT_TOKENS,
                padding="longest"
            ).to(self.device)

            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=settings.MAX_NEW_TOKENS,
                    do_sample=True,
                    temperature=settings.GENERATION_TEMPERATURE,
                    top_p=settings.GENERATION_TOP_P,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )

            text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            if text.startswith(prompt):
                return text[len(prompt):].strip()
            return text.strip()

        except Exception as e:
            logger.error("LLMService.generate() error", exc_info=True)
            return (
                "I'm sorry, I'm having trouble generating a response right now. "
                "Please try again in a moment or reach out to support@cartoncaps.com."
            )