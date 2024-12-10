using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class DemoManager : MonoBehaviour
{
    public GameObject nextButton;
    public GameObject backButton;
    public GameObject cursorObj;
    public GameObject guideText;
    public GameObject narrationPanel;
    public GameObject narrationText;
    public GameObject self; // Reference to the button itself
    public float waitTime; // Wait time from the press of the start button to the start of the lesson
    public static Animator actualAnimator;
    public static Animator shadowAnimator;

    void Start()
    {
        self.GetComponent<Button>().interactable = false; // Initially the start button is unpressable without any instance of an object
    }

    void Update()
    {
         // Reference the animator of the latest instances of the objects
        actualAnimator = NewCursor.actualObj.GetComponent<Animator>();
        shadowAnimator = NewCursor.shadowObj.GetComponent<Animator>();

        if (actualAnimator != null) // Check if there exists an instance of an object
        {
            self.GetComponent<Button>().interactable = true;
        }
    }

    public void EnterLesson()
    {
        StartCoroutine(LessonCoroutine());  
    }

    IEnumerator LessonCoroutine()
    {
        Destroy(cursorObj);
        Destroy(guideText);

        Image buttonImage = self.GetComponent<Image>();

        if (buttonImage != null)
        {
            Color initialColor = buttonImage.color;
            float elapsedTime = 0f;

            while (elapsedTime < waitTime)
            {
                elapsedTime += Time.deltaTime;
                float alpha = Mathf.Lerp(1f, 0f, elapsedTime / waitTime);

                buttonImage.color = new Color(initialColor.r, initialColor.g, initialColor.b, alpha);

                yield return null;
            }

            // Ensure fully transparent
            buttonImage.color = new Color(initialColor.r, initialColor.g, initialColor.b, 0f);
        }

        // Fade in lesson components
        narrationPanel.GetComponent<FadeIn>().StartFade();
        narrationText.GetComponent<FadeIn>().StartFade();
        nextButton.GetComponent<FadeIn>().StartFade();
        backButton.GetComponent<FadeIn>().StartFade();

        actualAnimator.SetBool("hasStarted", true);
        shadowAnimator.SetBool("hasStarted", true);
        
        Destroy(self); // Destroy the button once lesson is started
    }
}
