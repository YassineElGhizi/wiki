from deepl import deepl

t = deepl.DeepLCLI("en", "ja")
print(t.translate("hello"))