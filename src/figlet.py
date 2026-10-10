import pyfiglet

fig_text = ""

def render_text(text, font="Broadway KB"):
    return pyfiglet.figlet_format(text, font=font)

def set_buffer(fig_text):
    array = []
    lines = render_text(fig_text)
    for line in lines.split("\n"):
        # DEBUG: print(f"Line {lines.split('\n').index(line)}: {line}")
        array.append(line)

    return array


if __name__ == "__main__":
    fig_text = "Grey Forest"
    buffer = set_buffer(fig_text)
    for line in buffer:
        print(line)
