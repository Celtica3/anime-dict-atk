from time import sleep
from AnimeDictAtk import load, Anime, AnimeMeta
import click
from click_shell import shell

@shell(prompt=">>> ", intro="Welcome to AnimeDictAtk")
def main():
    load()
    print("type in the number of letters with space, for example: 3 4 5 is 3 letters, 4 letters, 5 letters")

@main.command(name="match")
@click.argument("format", type=str)
@click.option("--cont", "-c", is_flag=True, help="continue to match")   
@click.option("--vomit", "-v", is_flag=True, help="vomit all matches")
def match(format, cont, vomit):
    format = format.split(" ")
    format_str = ""
    for i in format:
        i = int(i)
        format_str += "".join(["1" for _ in range(i)])
        format_str += "0"
    
    format_str = format_str[:-1]
    for x in Anime.match_format(format_str):
        click.echo(x)
        if not cont and not vomit:
            break
        if vomit:
            sleep(0.5)
            continue
        if click.confirm("Continue?", abort=True):
            continue
    
if __name__ == "__main__":
    main()