import openai
import webbrowser
import os

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_website_url(query):
    # Prompt for the LLM
    prompt = f"Based on the user query '{query}', suggest a specific website URL that would be most relevant and helpful. Only return the URL, nothing else."

    # Call the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are a helpful assistant that suggests relevant website URLs based on user queries."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract the URL from the response
    suggested_url = response.choices[0].message.content.strip()

    return suggested_url


def open_website(url):
    webbrowser.open(url)


def main():
    while True:
        query = input("Enter your query (or 'quit' to exit): ")

        if query.lower() == 'quit':
            break

        try:
            url = get_website_url(query)
            print(f"Opening: {url}")
            open_website(url)
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()