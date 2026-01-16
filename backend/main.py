from agent import create_wuwa_agent

def main():
    """Simple CLI for testing the agent."""
    print("Wuthering Waves Build Advisor")
    print("=" * 50)
    print("Type 'quit' to exit\n")
    
    # Initialize agent
    agent = create_wuwa_agent()
    
    # Interactive loop
    while True:
        user_input = input("\n Ask anything: ").strip()
        
        # Exit conditions
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        # Run agent
        try:
            # LangGraph agents use streaming by default
            # We'll collect all events and show the final result
            print("\n" + "="*50)
            print("Thinking...")
            print("="*50)
            
            final_response = None
            
            # Stream events from the agent
            for event in agent.stream(
                {"messages": [{"role": "user", "content": user_input}]},
                stream_mode="values"
            ):
                # Get the last message in the state
                if "messages" in event:
                    last_message = event["messages"][-1]
                    
                    # Check if it's a tool call or final answer
                    if hasattr(last_message, 'content') and last_message.content:
                        final_response = last_message.content
            
            # Print final answer
            if final_response:
                print(f"\nAnswer:\n{final_response}\n")
            else:
                print("\n No response generated\n")
            
        except Exception as e:
            print(f"\nError: {str(e)}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()