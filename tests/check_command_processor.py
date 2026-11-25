from core.command_processor import CommandProcessor

processor = CommandProcessor()

while True:

    command = input("You: ")

    if command.lower().strip() == "exit":
        break

    response = processor.process(command)

    print(f"MAYA: {response}")