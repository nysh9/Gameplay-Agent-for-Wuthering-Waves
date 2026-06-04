from agent import create_wuwa_agent, build_rag_prompt

def main():
    """Simple CLI for testing the agent."""
    print("Wuthering Waves Build Advisor")
    print("=" * 50)
    print("Type 'quit' to exit\n")
    
    # Initialize agent
    agent = create_wuwa_agent()
    
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
            print("\n" + "="*50)
            print("Thinking...")
            print("="*50)
            
            final_response = None
            rag_prompt = build_rag_prompt(user_input)
            for event in agent.stream(
                {"messages": [{"role": "user", "content": rag_prompt}]},
                stream_mode="values"
            ):
                if "messages" in event:
                    last_message = event["messages"][-1]
                    if hasattr(last_message, 'content') and last_message.content:
                        final_response = last_message.content
            
            # final answer
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