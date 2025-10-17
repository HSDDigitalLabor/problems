import check50
from re import escape

FILE_NAME = "zahlenjagd.py"


@check50.check()
def exists():
    """Datei existiert"""
    check50.exists(FILE_NAME)

    # The hard-coded number 4 is the answer to the game (specified in test.py).
    # This is the number that the user is trying to guess.
    check50.include("checks/testing.py")


@check50.check(exists)
def test_string_shot():
    """zahlenjagd.py lehnt nicht-numerischen Schuss ab"""
    check50.run(f"python3 {FILE_NAME}").stdin("cat", prompt=True).stdout(
        regex("Schuss"), "Gib einen Schuss ab:"
    ).kill()


@check50.check(exists)
def test_integer_shot():
    """zahlenjagd.py lehnt Schuss außerhalb des Bereichs ab"""
    check50.run(f"python3 {FILE_NAME}").stdin("0", prompt=True).stdout(
        regex("Schuss"), "Gib einen Schuss ab:"
    ).kill()


@check50.check(exists)
def test_valid_shot():
    """zahlenjagd.py akzeptiert gültigen Schuss"""
    check50.run(f"python3 {FILE_NAME}").stdin("10", prompt=True).stdout(
        regex("Schuss"), "Gib einen Schuss ab:", regex=True
    ).kill()


@check50.check(test_valid_shot)
def test_string_guess():
    """zahlenjagd.py lehnt nicht-numerischen Schuss ab"""
    check50.run(f"python3 {FILE_NAME}").stdin("dog", prompt=True
    ).reject()


@check50.check(test_valid_shot)
def test_out_of_range_large():
    """zahlenjagd.py lehnt Schuss oberhalb des Bereichs mit \"Zu hoch!\" ab"""
    output = "Zu hoch!"
    check50.run("python3 testing.py").stdin("8", prompt=True
    ).stdout(regex(output), output, regex=True).reject()


@check50.check(test_valid_shot)
def test_nonpositive_shot():
    """zahlenjagd.py lehnt nicht-positive Schüsse ab"""
    check50.run(f"python3 {FILE_NAME}").stdin("0", prompt=True
    ).stdout(reject_regex("1 und 100"),
              "Bitte gib eine Zahl zwischen 1 und 100 ein.").kill()
    check50.run(f"python3 {FILE_NAME}").stdin("-50", prompt=True
    ).stdout(reject_regex("1 und 100"),
              "Bitte gib eine Zahl zwischen 1 und 100 ein.").kill()


@check50.check(test_valid_shot)
def test_too_large():
    """zahlenjagd.py gibt \"Zu hoch!\" aus, wenn der Schuss zu groß ist"""
    output = "Zu hoch!"
    check50.run("python3 testing.py").stdin("18", prompt=True
    ).stdout(regex(output), output, regex=True).reject()


@check50.check(test_valid_shot)
def test_just_right():
    """zahlenjagd.py gibt \"Volltreffer!\" aus, wenn der Schuss korrekt ist"""
    output = "Volltreffer!"
    check50.run("python3 testing.py").stdin("4", prompt=True
    ).stdout(regex(output), output, regex=True).exit()


@check50.check(test_valid_shot)
def test_too_small():
    """zahlenjagd.py gibt \"Zu niedrig!\" aus, wenn der Schuss zu klein ist"""
    output = "Zu niedrig!"
    check50.run("python3 testing.py").stdin("2", prompt=True
    ).stdout(regex(output), output, regex=True).reject()


def regex(text):
    """Case-insensitiv mit beliebigen Zeichen davor und danach matchen"""
    return rf"(?i)^.*{escape(text)}.*$"


def reject_regex(text):
    """Regex, die ablehnt, falls vor dem erwarteten Text bereits Text ausgegeben wurde"""
    return rf"(?i)(?<!\n){escape(text)}"
