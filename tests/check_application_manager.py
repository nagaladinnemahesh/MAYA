from tools.application_manager import ApplicationManager


manager = ApplicationManager()


print("\nRegistered Application Executables:")

for key, application in manager.applications.items():

    executable = manager.find_executable(application)

    print(f"{application['name']}: {executable}")


print("\nApplication Status:")

for key, application in manager.applications.items():

    running = manager.is_application_running(key)

    print(f"{application['name']}: {running}")


print("\nRunning Registered Applications:")

for application in manager.get_running_applications():

    print(application["name"])


print("\nApplication Launch Test:")

print(manager.open_application("notepad"))


print("\nAlias Resolution Test:")

application = manager.resolve_application("vs code")

print(application["name"] if application else "Not found")


print("\nUnknown Application Test:")

print(manager.open_application("unknown application"))