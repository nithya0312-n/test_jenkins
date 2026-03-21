# your_script.py

def main():
    print("Hello Jenkins, this is a simple Python script!")

    # Write something to a log file so Jenkins can archive it
    with open("pipeline_output.log", "w") as f:
        f.write("Pipeline executed successfully.\n")
        f.write("Message: Hello Jenkins!\n")

if __name__ == "__main__":
    main()

