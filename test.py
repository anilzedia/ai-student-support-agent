import google.generativeai as genai

genai.configure(api_key="AIzaSyBB3Paev1oJFWtgB3gMMuV2pigi8_iC318")

model = genai.GenerativeModel("gemini-pro")

response = model.generate_content("Hello")

print(response.text)