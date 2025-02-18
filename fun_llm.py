from openai import OpenAI
import json


def extract_job_ad_sections(job_ad_content, OPENAI_API_KEY, openai_model="gpt-4o" ):
    """
    Extracts job advertisement content into structured sections: job description, technical skills, and soft skills.

    Args:
        job_ad_content (str): The content of the job advertisement.
        OPENAI_API_KEY (str): API key for authenticating with OpenAI's GPT model.
        openai_model (str, optional): The OpenAI model to use for extraction (default is "gpt-4o").

    Returns:
        dict: A JSON object containing the extracted sections: job description, technical skills, and soft skills.
    """

    # Create openai client
    client = OpenAI(api_key=OPENAI_API_KEY)

    system_content = """
    Your HR (human resources) specialist. User will give you job advertisement content. You need to extract content for following sections:
    * Job description. Provinding description of job responsibilities and tasks. If result of this segment is list, concatenate into one string, separated by semicolon','.
    * Technical skills. Skills required for this job possitions.If result of this segment is list, concatenate into one string, separated by semicolon','.
    * Soft skills. Non-technical skills required for this job possitions.If result of this segment is list, concatenate into one string, separated by semicolon','.

    Provide response in json format

    """

    response = client.chat.completions.create(
        model=openai_model,
        messages=[
        {
        "role": "system",
        "content": system_content
        },
        {
        "role": "user",
        "content": job_ad_content
        }
        ],
        response_format = { "type": "json_object" },
        temperature=0.5,         # Low creativity
        max_tokens=1000,          # Limit response length
    )

    return json.loads(response.choices[0].message.content)






def check_if_question_is_relevat_to_job_ad(job_ad_content, user_question, openai_model, OPENAI_API_KEY):
    # Create openai client
    client = OpenAI(api_key=OPENAI_API_KEY)

    system_content = """
    Your HR (human resources) specialist. User will give you job advertisement content. Your you will need to evaluate if user's questions is about same 

    """

    response = client.chat.completions.create(
        model=openai_model,
        messages=[
        {
        "role": "system",
        "content": system_content
        },
        {
        "role": "user",
        "content": job_ad_content
        }
        ],
        response_format = { "type": "json_object" },
        temperature=0.5,         # Low creativity
        max_tokens=1000,          # Limit response length
    )

    return json.loads(response.choices[0].message.content)