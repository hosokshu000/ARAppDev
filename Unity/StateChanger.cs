using UnityEngine;
using System.Diagnostics;
using System.Collections; // Remove after debug

public class StateChanger : MonoBehaviour
{
    public static Animator actualAnimator;
    public static Animator shadowAnimator;
    public static Animator[] animatorArr = new Animator[2]; // Animator array to store animator components of instances of prefab
    public string prevState;
    void Start()
    {
        // Get animator components of prefab instance
        actualAnimator = NewCursor.actualObj.GetComponent<Animator>();
        shadowAnimator = NewCursor.shadowObj.GetComponent<Animator>();

        // Instantiate animator array
        animatorArr[0] = actualAnimator;
        animatorArr[1] = shadowAnimator;
    }

    void Update() {
        if (Time.timeScale != 1) {
            XcodeLog($"Time.timeScale was not 1, setting to 1.");
            Time.timeScale = 1;
        }

        if (!actualAnimator.enabled)
        {
            actualAnimator.enabled = true;
            XcodeLog("Animator was disabled. Enabling it now.");
        }

        if (actualAnimator.speed == 0)
        {
            actualAnimator.speed = 1;
            XcodeLog("Animator speed was 0. Resetting to 1.");
        }

        if (actualAnimator.GetCurrentAnimatorClipInfo(0).Length > 0)
        {
            string currentStateName = actualAnimator.GetCurrentAnimatorClipInfo(0)[0].clip.name;

            if (prevState != currentStateName) {
                XcodeLog($"State Change! Current: {currentStateName}    Previous: {prevState}");
                prevState = currentStateName;
            }
        }
        else
        {
            XcodeLog("No active animation clip.");
        }


        // Find the most recently instantiated objects
        actualAnimator = NewCursor.actualObj.GetComponent<Animator>();
        shadowAnimator = NewCursor.shadowObj.GetComponent<Animator>();

        if (actualAnimator != null && shadowAnimator != null)
        {
            // Update values for animator array
            animatorArr[0] = actualAnimator;
            animatorArr[1] = shadowAnimator;
        }
        else
        {
            XcodeLog("Could not find latest objects");
        }
    }

    public void ChangePhase(int increment) // Increment: set to +1 for next button and -1 for back button
    {
        // Iterate through animator array to change Phase on both animator components
        foreach (Animator animator in animatorArr) {
            if (animator.parameters.Length > 0) // Check to make sure parameters exist
            {
                int currentPhase = animator.GetInteger("Phase");
                XcodeLog($"Current Phase: {currentPhase}");
                int newPhase = currentPhase + increment;
                animator.SetInteger("Phase", newPhase);
                XcodeLog($"New Phase: {animator.GetInteger("Phase")}");

                animator.Update(0f); // Refresh the animator to force animation change
            }
            else
            {
                XcodeLog("Animator does not have any parameters or the parameter is missing.");
            }
        }
    }

    [Conditional("UNITY_IOS")]
    private void XcodeLog(string message)
    {
        // This will appear in Xcode's console
        UnityEngine.iOS.Device.SetNoBackupFlag(Application.persistentDataPath + "/XcodeLog.txt");
        System.IO.File.AppendAllText(Application.persistentDataPath + "/XcodeLog.txt", message + "\n");
        
        // This will still appear in Unity's console during development
        UnityEngine.Debug.Log(message);
    }
}