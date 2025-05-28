
class AIModelInterface:
    """Base interface for all AI models used in the application."""
    
    def __init__(self, name, description, tier):
        """
        Initialize the AI model.
        
        Args:
            name (str): Name of the model
            description (str): Brief description of the model
            tier (str): Tier this model belongs to ('personal' or 'corporate')
        """
        self.name = name
        self.description = description
        self.tier = tier

    def generate_response(self, prompt, system_message=None):
        """
        Generate a response based on the given prompt.

        Args:
            prompt (str): The user prompt
            system_message (str, optional): System message to guide the model

        Returns:
            str: Generated response
        """
        raise NotImplementedError("Subclasses must implement this method")

    def get_info(self):
        """
        Get information about the model.

        Returns:
            dict: Model information
        """
        return {
            "name": self.name,
            "description": self.description,
            "tier": self.tier
        }


class GPT4Model(AIModelInterface):
    """Implementation for GPT-4 model (Corporate tier)."""

    def __init__(self):
        super().__init__(
            name="GPT-4",
            description="High-accuracy model with advanced reasoning capabilities",
            tier="corporate"
        )

    def generate_response(self, prompt, system_message=None):
        """
        Generate a response using GPT-4 API.
        """
        import openai
        import os
        from openai import OpenAI

        # Ensure API key is loaded
        api_key = os.getenv("OPENAI_API_KEY")
        
        # Create the OpenAI client
        client = OpenAI(api_key=api_key)

        # Make the actual API call using the new client interface
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_message or "You are a professional interviewer."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()


class GeminiModel(AIModelInterface):
    """Implementation for Gemini model (Personal tier)."""

    def __init__(self):
        super().__init__(
            name="Gemini",
            description="Cost-efficient Google AI model with good performance",
            tier="personal"
        )

    def generate_response(self, prompt, system_message=None):
        """
        Generate a response using Google's Gemini API.
        """
        import google.generativeai as genai
        import os

        # Ensure API key is loaded
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

        try:
            # Use Gemini 2.0 Flash model
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            # Format the prompt with system message
            formatted_prompt = f"{system_message or 'You are a professional interviewer.'}\n\nUser: {prompt}\n\nAssistant:"

            # Make the API call
            response = model.generate_content(formatted_prompt)

            # Return the generated text
            return response.text.strip()
        except Exception as e:
            return f"An error occurred: {str(e)}"


# Model registry to store all available models
class ModelRegistry:
    """Registry for all available AI models in the application."""

    def __init__(self):
        self.models = {}
        self.current_model = None

    def register_model(self, model):
        """
        Register a model in the registry.

        Args:
            model (AIModelInterface): Model to register
        """
        self.models[model.name] = model

        # Set as current model if none is selected
        if self.current_model is None:
            self.current_model = model.name

    def get_model(self, name=None):
        """
        Get a model by name or the current model if name is None.

        Args:
            name (str, optional): Name of the model to get

        Returns:
            AIModelInterface: The requested model
        """
        if name is None:
            return self.models[self.current_model]
        return self.models[name]

    def set_current_model(self, name):
        """
        Set the current model.

        Args:
            name (str): Name of the model to set as current

        Returns:
            bool: True if successful, False otherwise
        """
        if name in self.models:
            self.current_model = name
            return True
        return False

    def get_models_by_tier(self, tier):
        """
        Get all models for a specific tier.

        Args:
            tier (str): Tier to filter by ('personal' or 'corporate')

        Returns:
            list: List of models in the specified tier
        """
        return [model for model in self.models.values() if model.tier == tier]

    def get_all_models(self):
        """
        Get all registered models.

        Returns:
            list: List of all registered models
        """
        return list(self.models.values())


# Initialize the model registry with available models
def initialize_models():
    """
    Initialize and register all available models.

    Returns:
        ModelRegistry: Initialized model registry
    """
    registry = ModelRegistry()

    # Register models
    registry.register_model(GPT4Model())
    registry.register_model(GeminiModel())
    
    return registry