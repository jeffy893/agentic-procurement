from ask_claude import ask_claude

# Example usage (requires AWS credentials and Bedrock access)
if __name__ == "__main__":
    prompt = "What are the key considerations when evaluating raw material suppliers?"
    
    print("Sending prompt to Claude...")
    print(f"Prompt: {prompt}")
    print("\nResponse:")
    
    response = ask_claude(prompt)
    print(response)