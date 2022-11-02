def cipher(text, shift, encrypt=True):
    """
    Encrypts or decrypts a text using the Caesar cipher, given a numerical shift value.

    Parameters
    ----------
    text: string. The text that is encrypted or decrypted.
    shift: integer. Describes how many letters forward or backward we change the text by.
    encypt: boolean. Text string is encrypted if set to True, decrypted if set to false.

    Returns
    -------
    new_text. The text that has been encrypted, or descrypted

    Examples
    --------
    >>> from cipher_ml4837 import cipher
    >>> cipher('lol', 1, encrypt=True)
    "mpm"
    >>> cipher('mpm', 1, encrypt=False)
    "lol"
    """
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    new_text = ''
    for c in text:
        index = alphabet.find(c)
        if index == -1:
            new_text += c
        else:
            new_index = index + shift if encrypt == True else index - shift
            new_index %= len(alphabet)
            new_text += alphabet[new_index:new_index+1]
    return new_text
