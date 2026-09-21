

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def main():
    print("Hello form langchain course")
    information = """
Son Goku[nb 20] is a fictional character and the main protagonist of the Dragon Ball manga series created by Akira Toriyama. He is based on Sun Wukong (known as Son Gokū in Japan and the Monkey King in the West), a main character of the classic 16th-century Chinese novel Journey to the West, combined with influences from the Hong Kong action cinema of Jackie Chan and Bruce Lee. Goku made his debut in the first Dragon Ball chapter, Bulma and Son Goku,[nb 21][nb 22] originally published in Japan's Weekly Shōnen Jump magazine on December 3, 1984.[2]

Goku is introduced as an eccentric, monkey-tailed boy who practices martial arts and possesses superhuman strength. He meets Bulma and joins her on a journey to find the seven wish-granting Dragon Balls. Along the way, he finds new friends who follow him on his journey to become stronger. As Goku grows up, he becomes the Earth's mightiest warrior and battles a wide variety of villains with the help of his friends and family, while also gaining new allies in the process. Born under the name Kakarot,[nb 23][nb 24] as a member of the Saiyan race on Planet Vegeta, he is sent to Earth as an infant prior to his homeworld's destruction at the hands of Frieza. Upon his arrival on Earth, the infant is discovered by Son Gohan, who becomes the adoptive grandfather of the boy and gives him the name Goku. The boy is initially full of violence and aggression due to his Saiyan nature, until an accidental head injury turns him into a cheerful, carefree person. Grandpa Gohan's kindness and teachings help to further influence Goku, who later on names his first son Gohan in honor of him.

As the protagonist of Dragon Ball, Goku appears in most of the episodes, films, television specials and OVAs of the manga's anime adaptations (Dragon Ball, Dragon Ball Z) and sequels (Dragon Ball GT, Dragon Ball Super, Dragon Ball Daima), as well as many of the franchise's video games. Due to the series' international popularity, Goku became one of the most recognizable and iconic manga/anime characters worldwide. Outside the Dragon Ball franchise, Goku has made cameo appearances in Toriyama's self-parody series Neko Majin Z, has been the subject of other parodies, and has appeared in special events. Most Western audiences were introduced to the adult version of Goku featured in the Dragon Ball Z anime, which adapted the final 26 Dragon Ball manga volumes, as opposed to his initial appearance as a child due to the limited success of the first anime series overseas.[3]
"""
    summary_template = """
    given ther information {information} I want you to create:
    1. A short summary
    2. two instresting fact about them
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatGoogleGenerativeAI( model="gemini-3.8-flash")
    chain = summary_prompt_template | llm

    response = chain.invoke(input={"information": information})
    print(response.content)

if __name__ == "__main__":
    main()