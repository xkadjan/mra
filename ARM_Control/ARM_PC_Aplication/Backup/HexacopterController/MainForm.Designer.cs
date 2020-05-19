namespace HexacopterController
{
    partial class MainForm
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

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.textBoxConsole = new System.Windows.Forms.TextBox();
            this.buttonSendCommand = new System.Windows.Forms.Button();
            this.textBoxYaw = new System.Windows.Forms.TextBox();
            this.textBoxPitch = new System.Windows.Forms.TextBox();
            this.textBoxRoll = new System.Windows.Forms.TextBox();
            this.textBoxThrottle = new System.Windows.Forms.TextBox();
            this.buttonReset = new System.Windows.Forms.Button();
            this.simpleSerialPort = new SimpleSerialPort.SimpleSerialPort();
            this.labelYaw = new System.Windows.Forms.Label();
            this.labelPitch = new System.Windows.Forms.Label();
            this.labelRoll = new System.Windows.Forms.Label();
            this.labelThrottle = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // textBoxConsole
            // 
            this.textBoxConsole.Location = new System.Drawing.Point(194, 13);
            this.textBoxConsole.Multiline = true;
            this.textBoxConsole.Name = "textBoxConsole";
            this.textBoxConsole.Size = new System.Drawing.Size(299, 226);
            this.textBoxConsole.TabIndex = 1;
            // 
            // buttonSendCommand
            // 
            this.buttonSendCommand.Location = new System.Drawing.Point(593, 117);
            this.buttonSendCommand.Name = "buttonSendCommand";
            this.buttonSendCommand.Size = new System.Drawing.Size(100, 23);
            this.buttonSendCommand.TabIndex = 2;
            this.buttonSendCommand.Text = "Send Command";
            this.buttonSendCommand.UseVisualStyleBackColor = true;
            this.buttonSendCommand.Click += new System.EventHandler(this.buttonVersion_Click);
            // 
            // textBoxYaw
            // 
            this.textBoxYaw.Location = new System.Drawing.Point(593, 12);
            this.textBoxYaw.Name = "textBoxYaw";
            this.textBoxYaw.Size = new System.Drawing.Size(100, 20);
            this.textBoxYaw.TabIndex = 3;
            this.textBoxYaw.Text = "0";
            // 
            // textBoxPitch
            // 
            this.textBoxPitch.Location = new System.Drawing.Point(593, 39);
            this.textBoxPitch.Name = "textBoxPitch";
            this.textBoxPitch.Size = new System.Drawing.Size(100, 20);
            this.textBoxPitch.TabIndex = 4;
            this.textBoxPitch.Text = "0";
            // 
            // textBoxRoll
            // 
            this.textBoxRoll.Location = new System.Drawing.Point(593, 65);
            this.textBoxRoll.Name = "textBoxRoll";
            this.textBoxRoll.Size = new System.Drawing.Size(100, 20);
            this.textBoxRoll.TabIndex = 5;
            this.textBoxRoll.Text = "0";
            // 
            // textBoxThrottle
            // 
            this.textBoxThrottle.Location = new System.Drawing.Point(593, 91);
            this.textBoxThrottle.Name = "textBoxThrottle";
            this.textBoxThrottle.Size = new System.Drawing.Size(100, 20);
            this.textBoxThrottle.TabIndex = 6;
            this.textBoxThrottle.Text = "0";
            // 
            // buttonReset
            // 
            this.buttonReset.Location = new System.Drawing.Point(593, 147);
            this.buttonReset.Name = "buttonReset";
            this.buttonReset.Size = new System.Drawing.Size(100, 23);
            this.buttonReset.TabIndex = 7;
            this.buttonReset.Text = "Reset";
            this.buttonReset.UseVisualStyleBackColor = true;
            this.buttonReset.Click += new System.EventHandler(this.buttonReset_Click);
            // 
            // simpleSerialPort
            // 
            this.simpleSerialPort.Location = new System.Drawing.Point(13, 13);
            this.simpleSerialPort.Name = "simpleSerialPort";
            this.simpleSerialPort.Size = new System.Drawing.Size(175, 226);
            this.simpleSerialPort.TabIndex = 0;
            // 
            // labelYaw
            // 
            this.labelYaw.AutoSize = true;
            this.labelYaw.Location = new System.Drawing.Point(505, 19);
            this.labelYaw.Name = "labelYaw";
            this.labelYaw.Size = new System.Drawing.Size(82, 13);
            this.labelYaw.TabIndex = 8;
            this.labelYaw.Text = "Yaw [-128, 127]";
            // 
            // labelPitch
            // 
            this.labelPitch.AutoSize = true;
            this.labelPitch.Location = new System.Drawing.Point(505, 46);
            this.labelPitch.Name = "labelPitch";
            this.labelPitch.Size = new System.Drawing.Size(82, 13);
            this.labelPitch.TabIndex = 9;
            this.labelPitch.Text = "Pitch [-128,127]";
            // 
            // labelRoll
            // 
            this.labelRoll.AutoSize = true;
            this.labelRoll.Location = new System.Drawing.Point(508, 71);
            this.labelRoll.Name = "labelRoll";
            this.labelRoll.Size = new System.Drawing.Size(76, 13);
            this.labelRoll.TabIndex = 10;
            this.labelRoll.Text = "Roll [-128,127]";
            // 
            // labelThrottle
            // 
            this.labelThrottle.AutoSize = true;
            this.labelThrottle.Location = new System.Drawing.Point(508, 97);
            this.labelThrottle.Name = "labelThrottle";
            this.labelThrottle.Size = new System.Drawing.Size(79, 13);
            this.labelThrottle.TabIndex = 11;
            this.labelThrottle.Text = "Throttle [0,255]";
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(705, 254);
            this.Controls.Add(this.labelThrottle);
            this.Controls.Add(this.labelRoll);
            this.Controls.Add(this.labelPitch);
            this.Controls.Add(this.labelYaw);
            this.Controls.Add(this.buttonReset);
            this.Controls.Add(this.textBoxThrottle);
            this.Controls.Add(this.textBoxRoll);
            this.Controls.Add(this.textBoxPitch);
            this.Controls.Add(this.textBoxYaw);
            this.Controls.Add(this.buttonSendCommand);
            this.Controls.Add(this.textBoxConsole);
            this.Controls.Add(this.simpleSerialPort);
            this.Name = "MainForm";
            this.Text = "Hexacopter Remote Control";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private SimpleSerialPort.SimpleSerialPort simpleSerialPort;
        private System.Windows.Forms.TextBox textBoxConsole;
        private System.Windows.Forms.Button buttonSendCommand;
        private System.Windows.Forms.TextBox textBoxYaw;
        private System.Windows.Forms.TextBox textBoxPitch;
        private System.Windows.Forms.TextBox textBoxRoll;
        private System.Windows.Forms.TextBox textBoxThrottle;
        private System.Windows.Forms.Button buttonReset;
        private System.Windows.Forms.Label labelYaw;
        private System.Windows.Forms.Label labelPitch;
        private System.Windows.Forms.Label labelRoll;
        private System.Windows.Forms.Label labelThrottle;
    }
}

