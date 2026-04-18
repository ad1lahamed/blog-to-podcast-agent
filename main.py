import os
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.eleven_labs import ElevenLabsTools
from agno.tools.firecrawl import FirecrawlTools
from agno.run.agent import RunOutput
from agno.utils.audio import write_audio_to_file
from agno.utils.log import logger
import streamlit as st
import uuid

st.set_page_config(page_title="blog to podcast")
st.title("agent")
st.sidebar.header("API keys")

gemini_api_key = st.sidebar.text_input("gemini api key", type="password")
elevenlabs_api_key = st.sidebar.text_input("elevenlabs api key", type="password")
firecrawl_api_key = st.sidebar.text_input("firecrawl api key", type="password")

keys_provided = all([gemini_api_key,elevenlabs_api_key,firecrawl_api_key])


url = st.text_input("enter url of the site")

generate_button = st.button("Generate audio" , disabled= not keys_provided)

if not keys_provided:
    st.warning("pls enter keys")

if generate_button:
    if url.strip()== "":
        st.warning("pls enter correct url")
    else:
        os.environ["GOOGLE_API_KEY"] = gemini_api_key
        os.environ["ELEVEN_LABS_API_KEY"] = elevenlabs_api_key
        os.environ["FIRECRAWL_API_KEY"] = firecrawl_api_key

        with st.spinner("Proccessing"):
            try:
                blog_to_podcast = Agent(
                    name = "blog to podcast",
                    id = "blog_to_podcast_agent",
                    model=Gemini(id="gemini-2.0-flash"),
                    tools=[
                        ElevenLabsTools(
                            voice_id="JBFqnCBsd6RMkjVDRZzb",
                            model_id="eleven_multilingual_v2",
                            target_directory="audio_generations",

                        ),
                        FirecrawlTools(),
                    ],
                    description="You are an AI agent that can generate audio using ElevenLabs API.",
                    instructions=[
                        "When the user provides a blog post URL, ",
                        "1. Use Firecrawltools to scrape the blog content.",
                        "2. Create a concise the summary of the blog content that is no more than 1000 characters.",
                        "3. It should cover all main points while making it engaging and conversational. ",
                        "4. Use ElevenLabsTools to convert the summary to audio files",
                        "Ensure that the summary is within 1000 character limit."
                    ],
                    markdown=True,
                    
                )

                podcast : RunOutput = blog_to_podcast.run(
                    f"COnver the blog content to a podcast : {url}"
                )
                

                save_dir = "audio_generations"
                os.makedirs(save_dir,exist_ok=True)

                if podcast.response_audio and len(podcast.response_audio)>0:
                    file_name = f"{save_dir}/podcast_{uuid.uuid4()}.wav"
                    write_audio_to_file(
                        audio=podcast.audio[0].base_64_audio,
                        filename=file_name
                    )

                    st.success("Audio generated successfully!")
                    audio_bytes = open(file_name,"rb").read()
                    st.audio(audio_bytes, format="audio/wav")

                else:
                    st.error("Audio generation failed. No audio content returned.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}"),
                logger.error(f"Error during audio generation: {str(e)}")    