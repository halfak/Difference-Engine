def confirm(question, default=None, stream=sys.stdout)
    """
    Prompts the user to respond yes or no.
    """
    question = str(question)
    options = {"yes": True, "y": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower().strip()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            stream.write("Please respond with 'yes' or 'no' "
                         "(or 'y' or 'n').\n")
