
class TestShortPhrase():
    def test_short_phrase(self):
        phrase = input("Введите строку длиной менее 15 символов:")
        n = len(phrase)
        assert n<15, f"Фраза должна быть короче 15 символов, длина строки '{phrase}' - {n} символов"
