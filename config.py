import json
import os
class Config:


    def Load(api):

        temp = """
export const defaultConfig = {
  // API key
  apiKey:""" + f"'{api}'" + """,

  // Your Developer appId, Apply in dashboard's developer section
  appId: '',

  // Is the extension enabled by default or not
  useCapsolver: true,

  // Solve captcha manually
  manualSolving: false,

  // Captcha solved callback function name
  solvedCallback: 'captchaSolvedCallback',

  // Use proxy or not
  // If useProxy is true, then proxyType, hostOrIp, port, proxyLogin, proxyPassword are required
  useProxy: false,
  proxyType: 'http',
  hostOrIp: '',
  port: '',
  proxyLogin: '',
  proxyPassword: '',

  enabledForBlacklistControl: false, // Use blacklist control
  blackUrlList: [], // Blacklist URL list

  // Is captcha enabled by default or not
  enabledForRecaptcha: false,
  enabledForRecaptchaV3: false,
  enabledForHCaptcha: false,
  enabledForFunCaptcha: true,
  enabledForImageToText: false,
  enabledForAwsCaptcha: false,

  // Task type: click or token
  reCaptchaMode: 'click',
  hCaptchaMode: 'click',

  // Delay before solving captcha
  reCaptchaDelayTime: 0,
  hCaptchaDelayTime: 0,
  textCaptchaDelayTime: 0,
  awsDelayTime: 0,

  // Number of repeated solutions after an error
  reCaptchaRepeatTimes: 10,
  reCaptcha3RepeatTimes: 10,
  hCaptchaRepeatTimes: 10,
  funCaptchaRepeatTimes: 10,
  textCaptchaRepeatTimes: 10,
  awsRepeatTimes: 10,

  // ReCaptcha V3 task type: ReCaptchaV3TaskProxyLess or ReCaptchaV3M1TaskProxyLess
  reCaptcha3TaskType: 'ReCaptchaV3TaskProxyLess',

  textCaptchaSourceAttribute: 'capsolver-image-to-text-source', // ImageToText source img's attribute name
  textCaptchaResultAttribute: 'capsolver-image-to-text-result', // ImageToText result element's attribute name
};
                """
        current_working_directory = os.getcwd()
        capsolver_extension_path = current_working_directory + r"\CapSolver.Browser.Extension-chrome-v1.11.0"
        with open(capsolver_extension_path + r"\assets\config.js", "w", encoding="utf-8") as file:
            file.write(temp)





        # Đóng file
        file.close()
    def Quest():
        print("Vui lòng nhập API Key CapSolver (Bỏ trống nếu bạn không muốn bypass Captcha): ")
        Api = input()
        if len(Api) == 0:
            print("Học cách lấy key free ở phần hướng dẫn")
            Api = ""
        
        Config.Load(Api)




    