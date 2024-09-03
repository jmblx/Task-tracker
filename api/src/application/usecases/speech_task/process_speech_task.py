# class ProcessSpeechTaskUseCase:
#     def __init__(self):
#         self.speech_client = YandexClient()
#         self.text_service = TextProcessingService()
#
#     async def execute(speech_text: str, api_key: str = "") -> str:
#         gigachat_bot = GigaChatBot()
#         input_dict = {"text": speech_text} | get_cur_date()
#         access_token = await gigachat_bot.get_access_token()
#         input_json = json.dumps(str(input_dict), ensure_ascii=False)
#         prompt = gigachat_bot.render(input_json)
#         return await gigachat_bot.get_response(prompt, access_token)
