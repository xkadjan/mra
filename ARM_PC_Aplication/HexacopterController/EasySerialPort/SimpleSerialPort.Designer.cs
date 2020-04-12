namespace SimpleSerialPort
{
    partial class SimpleSerialPort
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Component Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify 
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.comboBoxPortName = new System.Windows.Forms.ComboBox();
            this.buttonOpen = new System.Windows.Forms.Button();
            this.buttonClose = new System.Windows.Forms.Button();
            this.textBoxBaudRate = new System.Windows.Forms.TextBox();
            this.textBoxStatus = new System.Windows.Forms.TextBox();
            this.textBoxDataBits = new System.Windows.Forms.TextBox();
            this.comboBoxStopBits = new System.Windows.Forms.ComboBox();
            this.comboBoxParity = new System.Windows.Forms.ComboBox();
            this.labelStatus = new System.Windows.Forms.Label();
            this.labelPortName = new System.Windows.Forms.Label();
            this.labelBaudRate = new System.Windows.Forms.Label();
            this.labelDataBits = new System.Windows.Forms.Label();
            this.labelStopBits = new System.Windows.Forms.Label();
            this.labelParity = new System.Windows.Forms.Label();
            this.richTextBox1 = new System.Windows.Forms.RichTextBox();
            this.ReadTimeoutTextBox = new System.Windows.Forms.TextBox();
            this.WriteTimeoutTextBox = new System.Windows.Forms.TextBox();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // comboBoxPortName
            // 
            this.comboBoxPortName.FormattingEnabled = true;
            this.comboBoxPortName.Location = new System.Drawing.Point(101, 74);
            this.comboBoxPortName.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.comboBoxPortName.Name = "comboBoxPortName";
            this.comboBoxPortName.Size = new System.Drawing.Size(132, 24);
            this.comboBoxPortName.TabIndex = 0;
            // 
            // buttonOpen
            // 
            this.buttonOpen.BackColor = System.Drawing.Color.Green;
            this.buttonOpen.FlatStyle = System.Windows.Forms.FlatStyle.Popup;
            this.buttonOpen.ForeColor = System.Drawing.SystemColors.ControlLightLight;
            this.buttonOpen.Location = new System.Drawing.Point(20, 7);
            this.buttonOpen.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.buttonOpen.Name = "buttonOpen";
            this.buttonOpen.Size = new System.Drawing.Size(99, 28);
            this.buttonOpen.TabIndex = 1;
            this.buttonOpen.Text = "Open";
            this.buttonOpen.UseVisualStyleBackColor = false;
            this.buttonOpen.Click += new System.EventHandler(this.buttonOpen_Click);
            // 
            // buttonClose
            // 
            this.buttonClose.BackColor = System.Drawing.Color.Red;
            this.buttonClose.FlatStyle = System.Windows.Forms.FlatStyle.Popup;
            this.buttonClose.Location = new System.Drawing.Point(127, 7);
            this.buttonClose.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.buttonClose.Name = "buttonClose";
            this.buttonClose.Size = new System.Drawing.Size(108, 28);
            this.buttonClose.TabIndex = 2;
            this.buttonClose.Text = "Close";
            this.buttonClose.UseVisualStyleBackColor = false;
            this.buttonClose.Click += new System.EventHandler(this.buttonClose_Click);
            // 
            // textBoxBaudRate
            // 
            this.textBoxBaudRate.Location = new System.Drawing.Point(101, 107);
            this.textBoxBaudRate.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.textBoxBaudRate.Name = "textBoxBaudRate";
            this.textBoxBaudRate.Size = new System.Drawing.Size(132, 22);
            this.textBoxBaudRate.TabIndex = 3;
            // 
            // textBoxStatus
            // 
            this.textBoxStatus.Location = new System.Drawing.Point(101, 43);
            this.textBoxStatus.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.textBoxStatus.Name = "textBoxStatus";
            this.textBoxStatus.ReadOnly = true;
            this.textBoxStatus.Size = new System.Drawing.Size(132, 22);
            this.textBoxStatus.TabIndex = 4;
            // 
            // textBoxDataBits
            // 
            this.textBoxDataBits.Location = new System.Drawing.Point(101, 140);
            this.textBoxDataBits.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.textBoxDataBits.Name = "textBoxDataBits";
            this.textBoxDataBits.Size = new System.Drawing.Size(132, 22);
            this.textBoxDataBits.TabIndex = 5;
            // 
            // comboBoxStopBits
            // 
            this.comboBoxStopBits.FormattingEnabled = true;
            this.comboBoxStopBits.Location = new System.Drawing.Point(101, 174);
            this.comboBoxStopBits.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.comboBoxStopBits.Name = "comboBoxStopBits";
            this.comboBoxStopBits.Size = new System.Drawing.Size(132, 24);
            this.comboBoxStopBits.TabIndex = 6;
            // 
            // comboBoxParity
            // 
            this.comboBoxParity.FormattingEnabled = true;
            this.comboBoxParity.Location = new System.Drawing.Point(101, 208);
            this.comboBoxParity.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.comboBoxParity.Name = "comboBoxParity";
            this.comboBoxParity.Size = new System.Drawing.Size(132, 24);
            this.comboBoxParity.TabIndex = 7;
            // 
            // labelStatus
            // 
            this.labelStatus.AutoSize = true;
            this.labelStatus.Location = new System.Drawing.Point(44, 47);
            this.labelStatus.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.labelStatus.Name = "labelStatus";
            this.labelStatus.Size = new System.Drawing.Size(48, 17);
            this.labelStatus.TabIndex = 8;
            this.labelStatus.Text = "Status";
            // 
            // labelPortName
            // 
            this.labelPortName.AutoSize = true;
            this.labelPortName.Location = new System.Drawing.Point(17, 78);
            this.labelPortName.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.labelPortName.Name = "labelPortName";
            this.labelPortName.Size = new System.Drawing.Size(75, 17);
            this.labelPortName.TabIndex = 9;
            this.labelPortName.Text = "Port Name";
            // 
            // labelBaudRate
            // 
            this.labelBaudRate.AutoSize = true;
            this.labelBaudRate.Location = new System.Drawing.Point(16, 111);
            this.labelBaudRate.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.labelBaudRate.Name = "labelBaudRate";
            this.labelBaudRate.Size = new System.Drawing.Size(75, 17);
            this.labelBaudRate.TabIndex = 10;
            this.labelBaudRate.Text = "Baud Rate";
            this.labelBaudRate.Click += new System.EventHandler(this.labelBaudRate_Click);
            // 
            // labelDataBits
            // 
            this.labelDataBits.AutoSize = true;
            this.labelDataBits.Location = new System.Drawing.Point(27, 144);
            this.labelDataBits.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.labelDataBits.Name = "labelDataBits";
            this.labelDataBits.Size = new System.Drawing.Size(65, 17);
            this.labelDataBits.TabIndex = 11;
            this.labelDataBits.Text = "Data Bits";
            // 
            // labelStopBits
            // 
            this.labelStopBits.AutoSize = true;
            this.labelStopBits.Location = new System.Drawing.Point(28, 177);
            this.labelStopBits.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.labelStopBits.Name = "labelStopBits";
            this.labelStopBits.Size = new System.Drawing.Size(64, 17);
            this.labelStopBits.TabIndex = 12;
            this.labelStopBits.Text = "Stop Bits";
            // 
            // labelParity
            // 
            this.labelParity.AutoSize = true;
            this.labelParity.Location = new System.Drawing.Point(49, 212);
            this.labelParity.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.labelParity.Name = "labelParity";
            this.labelParity.Size = new System.Drawing.Size(44, 17);
            this.labelParity.TabIndex = 13;
            this.labelParity.Text = "Parity";
            // 
            // richTextBox1
            // 
            this.richTextBox1.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left)));
            this.richTextBox1.Location = new System.Drawing.Point(4, 305);
            this.richTextBox1.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.richTextBox1.Name = "richTextBox1";
            this.richTextBox1.ScrollBars = System.Windows.Forms.RichTextBoxScrollBars.ForcedVertical;
            this.richTextBox1.Size = new System.Drawing.Size(229, 106);
            this.richTextBox1.TabIndex = 14;
            this.richTextBox1.Text = "";
            // 
            // ReadTimeoutTextBox
            // 
            this.ReadTimeoutTextBox.Location = new System.Drawing.Point(101, 241);
            this.ReadTimeoutTextBox.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.ReadTimeoutTextBox.Name = "ReadTimeoutTextBox";
            this.ReadTimeoutTextBox.Size = new System.Drawing.Size(132, 22);
            this.ReadTimeoutTextBox.TabIndex = 16;
            // 
            // WriteTimeoutTextBox
            // 
            this.WriteTimeoutTextBox.Location = new System.Drawing.Point(101, 273);
            this.WriteTimeoutTextBox.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.WriteTimeoutTextBox.Name = "WriteTimeoutTextBox";
            this.WriteTimeoutTextBox.Size = new System.Drawing.Size(132, 22);
            this.WriteTimeoutTextBox.TabIndex = 17;
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(19, 245);
            this.label2.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(73, 17);
            this.label2.TabIndex = 18;
            this.label2.Text = "R Timeout";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(15, 277);
            this.label3.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(76, 17);
            this.label3.TabIndex = 19;
            this.label3.Text = "W Timeout";
            // 
            // SimpleSerialPort
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.Controls.Add(this.label3);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.WriteTimeoutTextBox);
            this.Controls.Add(this.ReadTimeoutTextBox);
            this.Controls.Add(this.richTextBox1);
            this.Controls.Add(this.labelParity);
            this.Controls.Add(this.labelStopBits);
            this.Controls.Add(this.labelDataBits);
            this.Controls.Add(this.labelBaudRate);
            this.Controls.Add(this.labelPortName);
            this.Controls.Add(this.labelStatus);
            this.Controls.Add(this.comboBoxParity);
            this.Controls.Add(this.comboBoxStopBits);
            this.Controls.Add(this.textBoxDataBits);
            this.Controls.Add(this.textBoxStatus);
            this.Controls.Add(this.textBoxBaudRate);
            this.Controls.Add(this.buttonClose);
            this.Controls.Add(this.buttonOpen);
            this.Controls.Add(this.comboBoxPortName);
            this.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.Name = "SimpleSerialPort";
            this.Size = new System.Drawing.Size(253, 447);
            this.Load += new System.EventHandler(this.SimpleSerialPort_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.ComboBox comboBoxPortName;
        private System.Windows.Forms.Button buttonOpen;
        private System.Windows.Forms.Button buttonClose;
        private System.Windows.Forms.TextBox textBoxBaudRate;
        private System.Windows.Forms.TextBox textBoxStatus;
        private System.Windows.Forms.TextBox textBoxDataBits;
        private System.Windows.Forms.ComboBox comboBoxStopBits;
        private System.Windows.Forms.ComboBox comboBoxParity;
        private System.Windows.Forms.Label labelStatus;
        private System.Windows.Forms.Label labelPortName;
        private System.Windows.Forms.Label labelBaudRate;
        private System.Windows.Forms.Label labelDataBits;
        private System.Windows.Forms.Label labelStopBits;
        private System.Windows.Forms.Label labelParity;
        private System.Windows.Forms.RichTextBox richTextBox1;
        private System.Windows.Forms.TextBox ReadTimeoutTextBox;
        private System.Windows.Forms.TextBox WriteTimeoutTextBox;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label3;
    }
}
