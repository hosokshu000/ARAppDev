using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class LessonNarrator : MonoBehaviour
{
    public TextMeshProUGUI textBox;
    public string[] text;
    public float narrationSpeed;
    int index; // Store current "position" in the narration text
    void Start()
    {
        textBox.text = ""; // Initially store an empty string
        StartNarration();
    }

    void Update()
    {
        
    }

    void StartNarration()
    {
        index = 0;
        StartCoroutine(WaitUntilFade());
    }

    // Wait until text is opaque to begin narration
    IEnumerator WaitUntilFade()
    {
        while (textBox.color.a != 1)
        {
            yield return null;
        }
        StartCoroutine(TypeText());
    }

    // Iterate and add more characters to the text in the textbox
    IEnumerator TypeText()
    {
        foreach (char c in text[index].ToCharArray())
        {
            textBox.text += c;
            yield return new WaitForSeconds(narrationSpeed);
        }
    }
}
