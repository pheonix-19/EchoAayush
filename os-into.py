import openai
import os
import platform
import subprocess

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_app_name(query):
    # Prompt for the LLM
    prompt = f"Based on the user query '{query}', suggest a specific application name that would be most relevant. Only return the application name, nothing else."

    # Call the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are a helpful assistant that suggests relevant application names based on user queries."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract the app name from the response
    suggested_app = response.choices[0].message.content.strip()

    return suggested_app


def open_app(app_name):
    system = platform.system()

    if system == "Windows":
        try:
            os.startfile(app_name)
        except FileNotFoundError:
            print(f"Could not find the application: {app_name}")
    elif system == "Darwin":  # macOS
        try:
            subprocess.call(["open", "-a", app_name])
        except subprocess.CalledProcessError:
            print(f"Could not open the application: {app_name}")
    elif system == "Linux":
        try:
            subprocess.Popen([app_name])
        except FileNotFoundError:
            print(f"Could not find the application: {app_name}")
    else:
        print(f"Unsupported operating system: {system}")


def main():
    while True:
        query = input("Enter your query for an app to open (or 'quit' to exit): ")

        if query.lower() == 'quit':
            break

        try:
            app_name = get_app_name(query)
            print(f"Attempting to open: {app_name}")
            open_app(app_name)
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()