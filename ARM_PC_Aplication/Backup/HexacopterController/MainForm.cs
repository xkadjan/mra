using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.Reflection;
using System.IO;
using System.Threading;

namespace HexacopterController
{
    public partial class MainForm : Form
    {
        SerialCommunicationManager serialCommunicationManager;
        public MainForm()
        {
            InitializeComponent();

            ConsoleWriter consoleWriter = new ConsoleWriter(textBoxConsole, 1000);
            Console.SetOut(consoleWriter);

            // Setup serial comms manager.
            serialCommunicationManager = new SerialCommunicationManager();
            serialCommunicationManager.MessageReceived += processMessage;

            // When the serial port is open tell the comms manager to listen.
            simpleSerialPort.PortOpened += serialCommunicationManager.Listen;
        }

        private void processMessage(byte[] message)
        {
            Console.WriteLine(new string(ASCIIEncoding.ASCII.GetChars(message, 0, message.Length)));
            byte[] encodedData = new byte[message.Length - 6];
            Buffer.BlockCopy(message, 3, encodedData, 0, encodedData.Length);
        }

        private delegate void SetControlPropertyThreadSafeDelegate(Control control, string propertyName, object propertyValue);
        public static void SetControlPropertyThreadSafe(Control control, string propertyName, object propertyValue)
        {
            if (control.InvokeRequired)
            {
                control.Invoke(new SetControlPropertyThreadSafeDelegate(SetControlPropertyThreadSafe), new object[] { control, propertyName, propertyValue });
            }
            else
            {
                control.GetType().InvokeMember(propertyName, BindingFlags.SetProperty, null, control, new object[] { propertyValue });
            }
        }

        private delegate void CallControlFunctionThreadSafeDelegate(Control control, string functionName);
        public static void CallControlFunctionThreadSafe(Control control, string functionName)
        {
            if (control.InvokeRequired)
            {
                control.Invoke(new CallControlFunctionThreadSafeDelegate(CallControlFunctionThreadSafe), new object[] { control, functionName });
            }
            else
            {
                control.GetType().InvokeMember(functionName, BindingFlags.InvokeMethod, null, control, null);
            }
        }

        private void buttonVersion_Click(object sender, EventArgs e)
        {

            try
            {
                sbyte yaw = Convert.ToSByte(textBoxYaw.Text);
                sbyte pitch = Convert.ToSByte(textBoxPitch.Text);
                sbyte roll = Convert.ToSByte(textBoxRoll.Text);
                byte throttle = Convert.ToByte(textBoxThrottle.Text);

                ExternControl cmd = new ExternControl(yaw, pitch, roll, throttle);
                byte[] message = FlightControllerMessage.CreateMessage('b', 1, cmd.Bytes);
                serialCommunicationManager.Send(message);
            }
            catch (OverflowException exc)
            {
                Console.WriteLine("The command in one of the text boxes is out of range.");
            }
            catch (InvalidOperationException exc)
            {
                Console.WriteLine("Could not read from serial port.  Is it open? Exception:" + exc.ToString());
            }
        }

        // Need to test communication? Example of a reset command: "#bR@T\r"
        private void buttonReset_Click(object sender, EventArgs e)
        {
            Stream serialStream = simpleSerialPort.Port.BaseStream;
            byte[] bytes = FlightControllerMessage.CreateMessage('R', 1);
            serialStream.Write(bytes, 0, bytes.Length);
        }
    }
}
