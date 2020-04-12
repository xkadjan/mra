using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Data;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.IO.Ports;
using System.IO;

namespace SimpleSerialPort
{
    public partial class SimpleSerialPort : UserControl
    {
        private SerialPort port;

        public event PortOpenedHandler PortOpened;
        public delegate void PortOpenedHandler(Stream stream);
        public SimpleSerialPort()
        {
            InitializeComponent();

            port = new SerialPort();
            port.ReadTimeout = 1000;
            port.WriteTimeout = 1000;
            textBoxStatus.Text = "closed";
            //textBoxBaudRate.Text = port.BaudRate.ToString();
            textBoxBaudRate.Text = "57600";
            textBoxDataBits.Text = port.DataBits.ToString();
            populateComboBoxes();
            setComboBoxDefaultValues();
        }

        public SerialPort Port
        {
            get
            {
                return port;
            }
        }

        private void buttonOpen_Click(object sender, EventArgs e)
        {
            try
            {
                if (port.IsOpen == true)
                    port.Close();

                port.PortName = comboBoxPortName.Text;
                port.BaudRate = Convert.ToInt32(textBoxBaudRate.Text);
                port.DataBits = Convert.ToInt32(textBoxDataBits.Text);
                port.StopBits = (StopBits)Enum.Parse(typeof(StopBits), comboBoxStopBits.Text);
                port.Parity = (Parity)Enum.Parse(typeof(Parity), comboBoxParity.Text);

                port.Open();
                textBoxStatus.Text = "open";
                if (PortOpened != null)
                {
                    PortOpened(port.BaseStream);
                }
            }
            catch (Exception ex)
            {
                textBoxStatus.Text = "error: " + ex;
            }
        }

        private void buttonClose_Click(object sender, EventArgs e)
        {
            port.Close();
            textBoxStatus.Text = "closed";
        }

        public string[] getPortNameValues()
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

        public string[] getStopBitValues()
        {
            return Enum.GetNames(typeof(StopBits));
        }

        public string[] getParityValues()
        {
            return Enum.GetNames(typeof(Parity));
        }

        private void populateComboBoxes()
        {
            comboBoxPortName.Items.AddRange(getPortNameValues());
            comboBoxStopBits.Items.AddRange(getStopBitValues());
            comboBoxParity.Items.AddRange(getParityValues());
        }

        private void setComboBoxDefaultValues()
        {
            try { comboBoxPortName.SelectedIndex = 0; }
            catch { }
            try { comboBoxStopBits.SelectedIndex = 1; }
            catch { }
            try { comboBoxParity.SelectedIndex = 0; }
            catch { }
        }
    }
}
