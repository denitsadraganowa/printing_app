import pickle
import requests
import json
import sys
class PurchaseGuideQuestionGenerator:
    def __init__(self, api_key, deployment_name, api_version="2024-08-01-preview", base_url=None):
        """
        Initialize the Purchase Guide Question Generator with API configurations.
        """
        self.api_key = api_key
        self.deployment_name = deployment_name
        self.api_version = api_version
        self.base_url = base_url or "https://ai-tombergman1893ai983820431027.openai.azure.com"
        self.headers = {
            'api-key': self.api_key,
            'Content-Type': 'application/json',
        }

    def generate_questions(self, product_type, num_questions=5, temperature=0.7):
        """
        Generate a list of non-technical guiding questions for users based on the product type.
        These questions should help users make informed purchasing decisions.
        """
        prompt = f"""
        Generate {num_questions} non-technical and helpful questions for a user who is considering purchasing a {product_type} on a website.
        The questions should guide the user to think about their needs, preferences, budget, and goals.
        Avoid technical details. Make the questions practical and user-friendly.
        """

        url = f"{self.base_url}/openai/deployments/{self.deployment_name}/chat/completions?api-version={self.api_version}"
        
        data = {
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 300,  
            "temperature": temperature
        }

        try:
            response = requests.post(url, headers=self.headers, data=json.dumps(data))
            response.raise_for_status() 
            result = response.json()

            if "choices" in result and len(result["choices"]) > 0:
                generated_text = result["choices"][0]["message"]["content"]
                questions = [q.strip() for q in generated_text.split("\n") if q.strip()]
                return questions
            else:
                print("No valid response received from the API.")
                return []
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return []



def save_to_pickle(model_instance, filename):
    with open(filename, 'wb') as f:
        pickle.dump(model_instance, f)
      



def load_from_pickle(filename):
    with open(filename, 'rb') as f:
        model_instance = pickle.load(f)
       
        return model_instance


if __name__ == "__main__":
  
    api_key = "DAwL81GZuK9Mug3ocvaahMVdPmjCuwSqDojcMAnd10Xfb5awn4DKJQQJ99AKACYeBjFXJ3w3AAAAACOGjD9x"
    deployment_name = "gpt-4o-mini"
    

    purchase_guide = PurchaseGuideQuestionGenerator(api_key, deployment_name)
    
   
    save_to_pickle(purchase_guide, 'purchase_guide_model.pkl')
    
 
    loaded_model = load_from_pickle('purchase_guide_model.pkl')
    
   
    product_type = sys.argv[1]
    
    questions = loaded_model.generate_questions(product_type, num_questions=5, temperature=0.8)
    
    if questions:
        print(f"Guiding Questions for buying a {product_type}:")
        for i, question in enumerate(questions, start=1):
            print(f"{i}. {question}")
    else:
        print("Failed to generate questions.")
