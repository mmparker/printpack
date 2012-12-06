


# Check for the existence of a "printed" folder
# If it doesn't exist, make it
if not os.path.exists(os.path.join(os.getcwd(), "printed")):
    os.makedirs(os.path.join(os.getcwd(), "printed"))

