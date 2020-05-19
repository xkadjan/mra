using System;
using System.Linq;
using System.Windows.Forms;
using System.IO.Ports;
using System.IO;

namespace SimpleSerialPort
{
    public partial class SimpleSerialPort : UserControl
    {
        private readonly SerialPort _port;

        public event PortOpenedHandler PortOpened;
        public delegate void PortOpenedHandler(Stream stream);
        public SimpleSerialPort()
        {
            InitializeComponent();

            _port = new SerialPort();
            ReadTimeoutTextBox.Text = "600000";
            WriteTimeoutTextBox.Text = "600000";
            textBoxStatus.Text = "closed";
            //textBoxBaudRate.Text = port.BaudRate.ToString();
            textBoxBaudRate.Text = "115200";
            textBoxDataBits.Text = _port.DataBits.ToString();
            PopulateComboBoxes();
            SetComboBoxDefaultValues();
        }

        public SerialPort Port
        {
            get
            {
                return _port;
            }
        }

        private void buttonOpen_Click(object sender, EventArgs e)
        {
            try
            {
                if (_port.IsOpen == true)
                    _port.Close();
                _port.ReadTimeout = Convert.ToInt32(ReadTimeoutTextBox.Text);
                _port.WriteTimeout = Convert.ToInt32(WriteTimeoutTextBox.Text);
                _port.PortName = comboBoxPortName.Text;
                _port.BaudRate = Convert.ToInt32(textBoxBaudRate.Text);
                _port.DataBits = Convert.ToInt32(textBoxDataBits.Text);
                _port.StopBits = (StopBits)Enum.Parse(typeof(StopBits), comboBoxStopBits.Text);
                _port.Parity = (Parity)Enum.Parse(typeof(Parity), comboBoxParity.Text);

                _port.Open();
                textBoxStatus.Text = "open";
                if (PortOpened != null)
                {
                    PortOpened(_port.BaseStream);
                }
            }
            catch (Exception ex)
            {
                textBoxStatus.Text = "close";
                richTextBox1.Text = "error: " + ex;
            }
        }

        private void buttonClose_Click(object sender, EventArgs e)
        {
            if (_port.IsOpen == true) {
                _port.Close();
                textBoxStatus.Text = "closed";
                richTextBox1.Text = "port is closed";
            }
            else
            {
                richTextBox1.Text = "port isn't opened";
            }
        }

        public string[] GetPortNameValues()
        {
            try
            {
                return SerialPort.GetPortNames().Reverse().ToArray();
            }
            catch
            {
                return new string[0];
            }
        }

        public string[] GetStopBitValues()
        {
            return Enum.GetNames(typeof(StopBits));
        }

        public string[] GetParityValues()
        {
            return Enum.GetNames(typeof(Parity));
        }

        private void PopulateComboBoxes()
        {
            comboBoxPortName.Items.AddRange(GetPortNameValues());
            comboBoxStopBits.Items.AddRange(GetStopBitValues());
            comboBoxParity.Items.AddRange(GetParityValues());
        }

        private void SetComboBoxDefaultValues()
        {
            try { comboBoxPortName.SelectedIndex = 0; }
            catch { }
            try { comboBoxStopBits.SelectedIndex = 1; }
            catch { }
            try { comboBoxParity.SelectedIndex = 0; }
            catch { }
        }

        private void SimpleSerialPort_Load(object sender, EventArgs e)
        {

        }

        private void labelBaudRate_Click(object sender, EventArgs e)
        {

        }
    }
}
