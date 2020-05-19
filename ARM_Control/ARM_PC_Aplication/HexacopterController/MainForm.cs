using System;
using System.Windows.Forms;
using System.Reflection;
using System.IO;
using System.Threading;
using System.Drawing;

namespace Controller
{
    public partial class MainForm : Form
    {
        private static SerialCommunicationManager _serialCommunicationManager;
        private static int _speed = 0;
        private static int _accel = 0;
        private bool recording = false;
        Thread controlSpeedThread = new Thread(ControlSpeed);
        
        public MainForm()
        {
            InitializeComponent();
            hScrollBarSpeed.Value = 0;

            #region Threads

            Thread.CurrentThread.Name = "Main thread";
            Console.WriteLine(Thread.CurrentThread.Name);

            ConsoleWriter consoleWriter = new ConsoleWriter(textBoxConsole, 20);
            Console.SetOut(consoleWriter);

            // Setup serial comms manager
            _serialCommunicationManager = new SerialCommunicationManager();
            _serialCommunicationManager.MessageReceived += ProcessMessage;

            // When the serial port is open tell the comms manager to listen.
            simpleSerialPort.PortOpened += _serialCommunicationManager.Listen;

            // Create _message 
            CheckForIllegalCrossThreadCalls = false;
            Thread controlThread = new Thread(Control);
            controlThread.Start();
            
            #endregion

        }

        #region Control

        public static void ControlSpeed()
        {
            
            
        }

        public void settext()
        {
            
        }

        public void Control()
        {
            
            while (true)
            {
                Thread.Sleep(100);
                textBoxNMEA.Text = _serialCommunicationManager.NMEA;
                if (_serialCommunicationManager.HALL)
                {
                    HallLed.BackColor = Color.Red;
                    textBoxArmSpeed.Text = _serialCommunicationManager.Speed.ToString();
                    _serialCommunicationManager.SetHALLFalse();
                }
                else {HallLed.BackColor = Color.DarkSlateGray;}

                if (_serialCommunicationManager.ENC)
                {
                    ENCLed.BackColor = Color.Red;
                    _serialCommunicationManager.SetENCFalse();
                }
                else { ENCLed.BackColor = Color.DarkSlateGray; }

                if (_serialCommunicationManager.PPS)
                {
                    PPSLed.BackColor = Color.Red;                    
                    _serialCommunicationManager.SetPPSFalse();
                }
                else { PPSLed.BackColor = Color.DarkSlateGray; }

                if (_serialCommunicationManager.Waiting || _serialCommunicationManager.Working)
                {
                    if (_serialCommunicationManager.Waiting)
                    {
                        StatusLed.BackColor = Color.Blue;
                        _serialCommunicationManager.SetWaitingFalse();
                    }

                    if (_serialCommunicationManager.Working)
                    {
                        StatusLed.BackColor = Color.Red;
                        _serialCommunicationManager.SetWorkingFalse();
                    }
                }
                else { StatusLed.BackColor = Color.DarkSlateGray; }


                textBox3.Text = _serialCommunicationManager.Mspeed.ToString();
                textBox2.Text = _serialCommunicationManager.M1.ToString();
                textBox4.Text = _serialCommunicationManager.M2.ToString();

            }
        }

        #endregion

        #region Rekvisitions

        private void ProcessMessage(byte[] message){}

        private delegate void SetControlPropertyThreadSafeDelegate(Control control, string propertyName, object propertyValue);

        public static void SetControlPropertyThreadSafe(Control control, string propertyName, object propertyValue)
        {
            if (control.InvokeRequired)
            {
                control.Invoke(new SetControlPropertyThreadSafeDelegate(SetControlPropertyThreadSafe),
                    new object[] { control, propertyName, propertyValue });
            }
            else
            {
                control.GetType()
                    .InvokeMember(propertyName, BindingFlags.SetProperty, null, control, new object[] { propertyValue });
            }
        }

        private delegate void CallControlFunctionThreadSafeDelegate(Control control, string functionName);

        public static void CallControlFunctionThreadSafe(Control control, string functionName)
        {
            if (control.InvokeRequired)
            {
                control.Invoke(new CallControlFunctionThreadSafeDelegate(CallControlFunctionThreadSafe),
                    new object[] { control, functionName });
            }
            else
            {
                control.GetType().InvokeMember(functionName, BindingFlags.InvokeMethod, null, control, null);
            }
        }

        // Need to test communication? Example of a reset command: "#bR@T\r"
 
        #endregion

        #region GUI

        private void TextBoxYaw_TextChanged(object sender, EventArgs e)
        {            
            
            if (textBoxSpeed.Text != "")
            {
                int i;
                bool bNum = int.TryParse(textBoxSpeed.Text, out i);
                if (bNum)
                {
                    if (Convert.ToInt16(textBoxSpeed.Text) >= -400 && Convert.ToInt16(textBoxSpeed.Text) <= 400)
                    {
                        hScrollBarSpeed.Value = Convert.ToInt16(textBoxSpeed.Text);
                        _speed = Convert.ToInt16(textBoxSpeed.Text);
                    }
                }
            }

            byte[] speed = BitConverter.GetBytes(hScrollBarSpeed.Value);
            Stream serialStream = simpleSerialPort.Port.BaseStream;
            byte[] bytes = FlightControllerMessage.CreateMessage('S', speed);
            serialStream.Write(bytes, 0, bytes.Length);
        }


        private void HScrollBarYaw_Scroll(object sender, ScrollEventArgs e)
        {
            textBoxSpeed.Text = hScrollBarSpeed.Value.ToString();
            _speed = hScrollBarSpeed.Value;
        }

        private void Button6_Click(object sender, EventArgs e){
            byte[] stop = {0};
            Stream serialStream = simpleSerialPort.Port.BaseStream;
            byte[] bytes = FlightControllerMessage.CreateMessage('P', stop);
            serialStream.Write(bytes, 0, bytes.Length);
        }

        #endregion

        private void ButtonFlyCommand_Click_1(object sender, EventArgs e)
        {
            byte[] waiting = {0};
            Stream serialStream1 = simpleSerialPort.Port.BaseStream;
            byte[] bytes1 = FlightControllerMessage.CreateMessage('W', waiting);
            serialStream1.Write(bytes1, 0, bytes1.Length);
            
            byte[] speed = BitConverter.GetBytes(hScrollBarSpeed.Value);
            Stream serialStream = simpleSerialPort.Port.BaseStream;
            byte[] bytes = FlightControllerMessage.CreateMessage('S', speed);
            serialStream.Write(bytes, 0, bytes.Length);
        }

        private void RecordingButton_Click(object sender, EventArgs e)
        {
            Stream serialStream = simpleSerialPort.Port.BaseStream;
            byte[] bytes;
            if (recording) {
                //RecordingButton.Text = "REC";
                byte[] stop = {0};
                bytes = FlightControllerMessage.CreateMessage('O', stop);
            }
            else {
                //RecordingButton.Text = "STOP";
                byte[] rec = {1};
                bytes = FlightControllerMessage.CreateMessage('O', rec);
            }
            serialStream.Write(bytes, 0, bytes.Length);
            recording = !recording;
        }

        private void MainForm_Load(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            textBoxNMEA.Text = "";
            _serialCommunicationManager.NMEA = "";
        }

        private void button2_Click(object sender, EventArgs e)
        {
            textBoxNMEA.Text = _serialCommunicationManager.NMEA;
        }

        private void button3_Click(object sender, EventArgs e)
        {

        }

        private void button1_Click_1(object sender, EventArgs e)
        {
            textBoxNMEA.Text = "";
            _serialCommunicationManager.NMEA = "";
        }

        private void button2_Click_1(object sender, EventArgs e)
        {
            byte[] breaking = { 1 };
            Stream serialStream1 = simpleSerialPort.Port.BaseStream;
            byte[] bytes1 = FlightControllerMessage.CreateMessage('B', breaking);
            serialStream1.Write(bytes1, 0, bytes1.Length);
        }

        private void button3_Click_1(object sender, EventArgs e)
        {
            byte[] breaking = { 0 };
            Stream serialStream1 = simpleSerialPort.Port.BaseStream;
            byte[] bytes1 = FlightControllerMessage.CreateMessage('B', breaking);
            serialStream1.Write(bytes1, 0, bytes1.Length);
        }

        private void hScrollBar1_Scroll(object sender, ScrollEventArgs e)
        {
            textBoxAccel.Text = hScrollBarAccel.Value.ToString();
            _accel = hScrollBarAccel.Value;
        }

        private void textBoxAccel_TextChanged(object sender, EventArgs e)
        {
            if (textBoxAccel.Text != "")
            {
                int i;
                bool bNum = int.TryParse(textBoxAccel.Text, out i);
                if (bNum)
                {
                    if (Convert.ToInt16(textBoxAccel.Text) >= 1 && Convert.ToInt16(textBoxAccel.Text) <= 10)
                    {
                        hScrollBarAccel.Value = Convert.ToInt16(textBoxAccel.Text);
                        _accel = Convert.ToInt16(textBoxAccel.Text);
                    }
                }            

            byte[] accel = BitConverter.GetBytes(hScrollBarAccel.Value);
            Stream serialStream = simpleSerialPort.Port.BaseStream;
            byte[] bytes = FlightControllerMessage.CreateMessage('A', accel);
            serialStream.Write(bytes, 0, bytes.Length);
            }
        }

        private void textBoxArmSpeed_TextChanged(object sender, EventArgs e)
        {

        }

        private void buttonRestartSynchro_Click(object sender, EventArgs e)
        {
            byte[] breaking = { 1 };
            Stream serialStream1 = simpleSerialPort.Port.BaseStream;
            byte[] bytes1 = FlightControllerMessage.CreateMessage('R', breaking);
            serialStream1.Write(bytes1, 0, bytes1.Length);
            textBoxNMEA.Text = "";
        }

        private void textBox3_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBoxNMEA_TextChanged(object sender, EventArgs e)
        {

        }
    }
}
