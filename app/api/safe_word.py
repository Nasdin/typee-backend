from app.models.word_data import WordData
from app.services.firebase import get_firestore_document, set_firestore_document
from app.services.openai import chat_completion


async def is_word_safe_firestore(word_data: WordData) -> bool:
    """
    Check if the word safety status is in Firestore for a given WordData object.

    Parameters:
    -----------
    word_data : WordData
        The WordData object containing the word to check the safety status for.

    Returns:
    --------
    bool
        True if the word is safe, False otherwise.

    Raises:
    -------
    IndexError
        If the word safety status is not found in Firestore.

    Example:
    --------
    >>> from app.models.word_data import WordData
    >>> word_data = WordData(word="dog")
    >>> await is_word_safe_firestore(word_data)
    True
    """
    # Check if the word safety status is in Firestore
    data = await get_firestore_document("safe_words", word_data.word)
    if data:
        return data["is_safe"]
    raise IndexError


async def update_word_safe_firestore(word_data: WordData, is_safe):
    """
        Update the word safety status in Firestore for a given WordData object.

        Parameters:
        -----------
        word_data : WordData
            The WordData object containing the word to update the safety status for.
        is_safe : bool
            The new safety status for the word.

        Returns:
        --------
        None

        Example:
        --------
        >>> from app.models.word_data import WordData
        >>> word_data = WordData(word="dog")
        >>> await update_word_safe_firestore(word_data, True)
        """
    await set_firestore_document("safe_words", word_data.word, {"is_safe": is_safe})


async def is_word_safe_find_out_from_openai(word_data: WordData):
    """
       Check if a given word is safe for children using the OpenAI API.

       Parameters:
       -----------
       word_data : WordData
           The WordData object containing the word to check the safety status for.

       Returns:
       --------
       bool
           True if the word is safe, False otherwise.

       Example:
       --------
       >>> from app.models.word_data import WordData
       >>> word_data = WordData(word="dog")
       >>> await is_word_safe_find_out_from_openai(word_data)
       True
       """
    prompt = f"Is the word '{word_data.word}' safe for children? Please answer yes or no."
    response = await chat_completion(prompt)
    result = response.strip().lower()
    return result == "yes" or result == "y"


async def is_word_safe(word_data: WordData):
    """
       Check if a given word is safe for children using both Firestore and the OpenAI API.

       Parameters:
       -----------
       word_data : WordData
           The WordData object containing the word to check the safety status for.

       Returns:
       --------
       bool
           True if the word is safe, False otherwise.

       Example:
       --------
       >>> from app.models.word_data import WordData
       >>> word_data = WordData(word="dog")
       >>> await is_word_safe(word_data)
       True
       """
    # Integrates both Firestore and OpenAI

    try:
        is_safe = await is_word_safe_firestore(word_data)
        return is_safe
    except IndexError:
        # Call OpenAI instead to find out
        is_safe = await is_word_safe_find_out_from_openai(word_data)
        await update_word_safe_firestore(word_data, is_safe)
        return is_safe
