Add-Type -AssemblyName System.speech
$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer
$speak.SetOutputToWaveFile("C:\Users\sajg_\AndroidStudioProjects\PhoenixAICore\muestras\audio_gerencia.wav")
$speak.Speak("Microservices architecture is a design pattern where applications are composed of small, independent services communicating over well-defined APIs.")
$speak.Dispose()
