using System.Windows.Forms;

namespace Controller
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(MainForm));
            this.buttonFlyCommand = new System.Windows.Forms.Button();
            this.groupBoxCommunication = new System.Windows.Forms.GroupBox();
            this.simpleSerialPort = new SimpleSerialPort.SimpleSerialPort();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.label11 = new System.Windows.Forms.Label();
            this.label10 = new System.Windows.Forms.Label();
            this.label9 = new System.Windows.Forms.Label();
            this.label8 = new System.Windows.Forms.Label();
            this.groupBox3 = new System.Windows.Forms.GroupBox();
            this.label12 = new System.Windows.Forms.Label();
            this.textBox3 = new System.Windows.Forms.TextBox();
            this.button1 = new System.Windows.Forms.Button();
            this.textBoxNMEA = new System.Windows.Forms.TextBox();
            this.label7 = new System.Windows.Forms.Label();
            this.label6 = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.textBox4 = new System.Windows.Forms.TextBox();
            this.textBox2 = new System.Windows.Forms.TextBox();
            this.textBoxArmSpeed = new System.Windows.Forms.TextBox();
            this.label4 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.label1 = new System.Windows.Forms.Label();
            this.StatusLed = new System.Windows.Forms.Button();
            this.PPSLed = new System.Windows.Forms.Button();
            this.ENCLed = new System.Windows.Forms.Button();
            this.HallLed = new System.Windows.Forms.Button();
            this.textBoxConsole = new System.Windows.Forms.TextBox();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            this.buttonRestartSynchro = new System.Windows.Forms.Button();
            this.textBoxAccel = new System.Windows.Forms.TextBox();
            this.button6 = new System.Windows.Forms.Button();
            this.groupBox4 = new System.Windows.Forms.GroupBox();
            this.hScrollBarAccel = new System.Windows.Forms.HScrollBar();
            this.textBoxSpeed = new System.Windows.Forms.TextBox();
            this.button3 = new System.Windows.Forms.Button();
            this.button2 = new System.Windows.Forms.Button();
            this.MovesGroupBox = new System.Windows.Forms.GroupBox();
            this.hScrollBarSpeed = new System.Windows.Forms.HScrollBar();
            this.groupBoxCommunication.SuspendLayout();
            this.groupBox1.SuspendLayout();
            this.groupBox3.SuspendLayout();
            this.groupBox2.SuspendLayout();
            this.groupBox4.SuspendLayout();
            this.MovesGroupBox.SuspendLayout();
            this.SuspendLayout();
            // 
            // buttonFlyCommand
            // 
            this.buttonFlyCommand.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.buttonFlyCommand.BackColor = System.Drawing.Color.Green;
            this.buttonFlyCommand.Font = new System.Drawing.Font("Microsoft Sans Serif", 14.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonFlyCommand.Location = new System.Drawing.Point(6, 110);
            this.buttonFlyCommand.Name = "buttonFlyCommand";
            this.buttonFlyCommand.Size = new System.Drawing.Size(310, 53);
            this.buttonFlyCommand.TabIndex = 2;
            this.buttonFlyCommand.Text = "Start";
            this.buttonFlyCommand.TextImageRelation = System.Windows.Forms.TextImageRelation.TextBeforeImage;
            this.buttonFlyCommand.UseVisualStyleBackColor = false;
            this.buttonFlyCommand.Click += new System.EventHandler(this.ButtonFlyCommand_Click_1);
            // 
            // groupBoxCommunication
            // 
            this.groupBoxCommunication.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left)));
            this.groupBoxCommunication.BackColor = System.Drawing.SystemColors.ActiveBorder;
            this.groupBoxCommunication.Controls.Add(this.simpleSerialPort);
            this.groupBoxCommunication.Location = new System.Drawing.Point(12, 12);
            this.groupBoxCommunication.Name = "groupBoxCommunication";
            this.groupBoxCommunication.Size = new System.Drawing.Size(186, 436);
            this.groupBoxCommunication.TabIndex = 41;
            this.groupBoxCommunication.TabStop = false;
            this.groupBoxCommunication.Text = "Communication";
            // 
            // simpleSerialPort
            // 
            this.simpleSerialPort.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left)));
            this.simpleSerialPort.Location = new System.Drawing.Point(-1, 19);
            this.simpleSerialPort.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.simpleSerialPort.Name = "simpleSerialPort";
            this.simpleSerialPort.Size = new System.Drawing.Size(184, 417);
            this.simpleSerialPort.TabIndex = 0;
            // 
            // groupBox1
            // 
            this.groupBox1.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.groupBox1.BackColor = System.Drawing.SystemColors.ActiveBorder;
            this.groupBox1.Controls.Add(this.label11);
            this.groupBox1.Controls.Add(this.label10);
            this.groupBox1.Controls.Add(this.label9);
            this.groupBox1.Controls.Add(this.label8);
            this.groupBox1.Controls.Add(this.groupBox3);
            this.groupBox1.Controls.Add(this.StatusLed);
            this.groupBox1.Controls.Add(this.PPSLed);
            this.groupBox1.Controls.Add(this.ENCLed);
            this.groupBox1.Controls.Add(this.HallLed);
            this.groupBox1.Location = new System.Drawing.Point(12, 455);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(510, 143);
            this.groupBox1.TabIndex = 42;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "State";
            // 
            // label11
            // 
            this.label11.AutoSize = true;
            this.label11.Location = new System.Drawing.Point(42, 115);
            this.label11.Name = "label11";
            this.label11.Size = new System.Drawing.Size(47, 13);
            this.label11.TabIndex = 84;
            this.label11.Text = "Encoder";
            // 
            // label10
            // 
            this.label10.AutoSize = true;
            this.label10.Location = new System.Drawing.Point(42, 28);
            this.label10.Name = "label10";
            this.label10.Size = new System.Drawing.Size(71, 13);
            this.label10.TabIndex = 83;
            this.label10.Text = "Comunication";
            // 
            // label9
            // 
            this.label9.AutoSize = true;
            this.label9.Location = new System.Drawing.Point(42, 57);
            this.label9.Name = "label9";
            this.label9.Size = new System.Drawing.Size(28, 13);
            this.label9.TabIndex = 82;
            this.label9.Text = "PPS";
            // 
            // label8
            // 
            this.label8.AutoSize = true;
            this.label8.Location = new System.Drawing.Point(42, 86);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(55, 13);
            this.label8.TabIndex = 81;
            this.label8.Text = "Hall probe";
            // 
            // groupBox3
            // 
            this.groupBox3.Controls.Add(this.label12);
            this.groupBox3.Controls.Add(this.textBox3);
            this.groupBox3.Controls.Add(this.button1);
            this.groupBox3.Controls.Add(this.textBoxNMEA);
            this.groupBox3.Controls.Add(this.label7);
            this.groupBox3.Controls.Add(this.label6);
            this.groupBox3.Controls.Add(this.label5);
            this.groupBox3.Controls.Add(this.textBox4);
            this.groupBox3.Controls.Add(this.textBox2);
            this.groupBox3.Controls.Add(this.textBoxArmSpeed);
            this.groupBox3.Controls.Add(this.label4);
            this.groupBox3.Controls.Add(this.label3);
            this.groupBox3.Controls.Add(this.label2);
            this.groupBox3.Controls.Add(this.label1);
            this.groupBox3.Location = new System.Drawing.Point(118, 0);
            this.groupBox3.Name = "groupBox3";
            this.groupBox3.Size = new System.Drawing.Size(387, 143);
            this.groupBox3.TabIndex = 76;
            this.groupBox3.TabStop = false;
            // 
            // label12
            // 
            this.label12.AutoSize = true;
            this.label12.BackColor = System.Drawing.SystemColors.Control;
            this.label12.Enabled = false;
            this.label12.Location = new System.Drawing.Point(116, 29);
            this.label12.Name = "label12";
            this.label12.Size = new System.Drawing.Size(32, 13);
            this.label12.TabIndex = 82;
            this.label12.Text = "km/h";
            // 
            // textBox3
            // 
            this.textBox3.Location = new System.Drawing.Point(232, 25);
            this.textBox3.Name = "textBox3";
            this.textBox3.Size = new System.Drawing.Size(89, 20);
            this.textBox3.TabIndex = 81;
            this.textBox3.Text = "10";
            this.textBox3.TextChanged += new System.EventHandler(this.textBox3_TextChanged);
            // 
            // button1
            // 
            this.button1.Location = new System.Drawing.Point(347, 96);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(34, 20);
            this.button1.TabIndex = 80;
            this.button1.Text = "cls";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.button1_Click_1);
            // 
            // textBoxNMEA
            // 
            this.textBoxNMEA.Location = new System.Drawing.Point(56, 97);
            this.textBoxNMEA.Name = "textBoxNMEA";
            this.textBoxNMEA.Size = new System.Drawing.Size(286, 20);
            this.textBoxNMEA.TabIndex = 79;
            this.textBoxNMEA.TextChanged += new System.EventHandler(this.textBoxNMEA_TextChanged);
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Location = new System.Drawing.Point(12, 100);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(38, 13);
            this.label7.TabIndex = 78;
            this.label7.Text = "NMEA";
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.BackColor = System.Drawing.SystemColors.Control;
            this.label6.Enabled = false;
            this.label6.Location = new System.Drawing.Point(299, 67);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(22, 13);
            this.label6.TabIndex = 77;
            this.label6.Text = "mA";
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.BackColor = System.Drawing.SystemColors.Control;
            this.label5.Enabled = false;
            this.label5.Location = new System.Drawing.Point(123, 64);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(22, 13);
            this.label5.TabIndex = 76;
            this.label5.Text = "mA";
            // 
            // textBox4
            // 
            this.textBox4.Location = new System.Drawing.Point(232, 63);
            this.textBox4.Name = "textBox4";
            this.textBox4.Size = new System.Drawing.Size(89, 20);
            this.textBox4.TabIndex = 74;
            this.textBox4.Text = "0";
            // 
            // textBox2
            // 
            this.textBox2.Location = new System.Drawing.Point(56, 63);
            this.textBox2.Name = "textBox2";
            this.textBox2.Size = new System.Drawing.Size(89, 20);
            this.textBox2.TabIndex = 73;
            this.textBox2.Text = "0";
            // 
            // textBoxArmSpeed
            // 
            this.textBoxArmSpeed.Location = new System.Drawing.Point(56, 27);
            this.textBoxArmSpeed.Name = "textBoxArmSpeed";
            this.textBoxArmSpeed.Size = new System.Drawing.Size(89, 20);
            this.textBoxArmSpeed.TabIndex = 72;
            this.textBoxArmSpeed.Text = "0";
            this.textBoxArmSpeed.TextChanged += new System.EventHandler(this.textBoxArmSpeed_TextChanged);
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Enabled = false;
            this.label4.Location = new System.Drawing.Point(161, 28);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(66, 13);
            this.label4.TabIndex = 71;
            this.label4.Text = "Motor speed";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Enabled = false;
            this.label3.Location = new System.Drawing.Point(184, 65);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(43, 13);
            this.label3.TabIndex = 70;
            this.label3.Text = "Motor 2";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Enabled = false;
            this.label2.Location = new System.Drawing.Point(8, 66);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(43, 13);
            this.label2.TabIndex = 69;
            this.label2.Text = "Motor 1";
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Enabled = false;
            this.label1.Location = new System.Drawing.Point(12, 30);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(38, 13);
            this.label1.TabIndex = 68;
            this.label1.Text = "Speed";
            // 
            // StatusLed
            // 
            this.StatusLed.BackColor = System.Drawing.Color.SlateGray;
            this.StatusLed.Location = new System.Drawing.Point(6, 19);
            this.StatusLed.Name = "StatusLed";
            this.StatusLed.Size = new System.Drawing.Size(30, 30);
            this.StatusLed.TabIndex = 74;
            this.StatusLed.UseVisualStyleBackColor = false;
            // 
            // PPSLed
            // 
            this.PPSLed.BackColor = System.Drawing.Color.SlateGray;
            this.PPSLed.Location = new System.Drawing.Point(6, 48);
            this.PPSLed.Name = "PPSLed";
            this.PPSLed.Size = new System.Drawing.Size(30, 30);
            this.PPSLed.TabIndex = 75;
            this.PPSLed.UseVisualStyleBackColor = false;
            // 
            // ENCLed
            // 
            this.ENCLed.BackColor = System.Drawing.Color.SlateGray;
            this.ENCLed.Location = new System.Drawing.Point(6, 106);
            this.ENCLed.Name = "ENCLed";
            this.ENCLed.Size = new System.Drawing.Size(30, 30);
            this.ENCLed.TabIndex = 72;
            this.ENCLed.UseVisualStyleBackColor = false;
            // 
            // HallLed
            // 
            this.HallLed.BackColor = System.Drawing.Color.SlateGray;
            this.HallLed.Location = new System.Drawing.Point(6, 77);
            this.HallLed.Name = "HallLed";
            this.HallLed.Size = new System.Drawing.Size(30, 30);
            this.HallLed.TabIndex = 73;
            this.HallLed.UseVisualStyleBackColor = false;
            this.HallLed.Click += new System.EventHandler(this.button3_Click);
            // 
            // textBoxConsole
            // 
            this.textBoxConsole.Location = new System.Drawing.Point(541, 563);
            this.textBoxConsole.Name = "textBoxConsole";
            this.textBoxConsole.Size = new System.Drawing.Size(72, 20);
            this.textBoxConsole.TabIndex = 75;
            this.textBoxConsole.Text = "Not connected";
            this.textBoxConsole.Visible = false;
            // 
            // groupBox2
            // 
            this.groupBox2.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.groupBox2.BackColor = System.Drawing.SystemColors.ActiveBorder;
            this.groupBox2.Controls.Add(this.buttonRestartSynchro);
            this.groupBox2.Controls.Add(this.textBoxAccel);
            this.groupBox2.Controls.Add(this.button6);
            this.groupBox2.Controls.Add(this.groupBox4);
            this.groupBox2.Controls.Add(this.textBoxSpeed);
            this.groupBox2.Controls.Add(this.button3);
            this.groupBox2.Controls.Add(this.button2);
            this.groupBox2.Controls.Add(this.MovesGroupBox);
            this.groupBox2.Controls.Add(this.buttonFlyCommand);
            this.groupBox2.FlatStyle = System.Windows.Forms.FlatStyle.Popup;
            this.groupBox2.Location = new System.Drawing.Point(201, 13);
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.Size = new System.Drawing.Size(321, 435);
            this.groupBox2.TabIndex = 43;
            this.groupBox2.TabStop = false;
            this.groupBox2.Text = "Arm control";
            // 
            // buttonRestartSynchro
            // 
            this.buttonRestartSynchro.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.buttonRestartSynchro.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(255)))), ((int)(((byte)(128)))), ((int)(((byte)(0)))));
            this.buttonRestartSynchro.Font = new System.Drawing.Font("Microsoft Sans Serif", 14.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonRestartSynchro.Location = new System.Drawing.Point(4, 228);
            this.buttonRestartSynchro.Name = "buttonRestartSynchro";
            this.buttonRestartSynchro.Size = new System.Drawing.Size(310, 53);
            this.buttonRestartSynchro.TabIndex = 61;
            this.buttonRestartSynchro.Text = "Restart synchro board";
            this.buttonRestartSynchro.TextImageRelation = System.Windows.Forms.TextImageRelation.TextBeforeImage;
            this.buttonRestartSynchro.UseVisualStyleBackColor = false;
            this.buttonRestartSynchro.Click += new System.EventHandler(this.buttonRestartSynchro_Click);
            // 
            // textBoxAccel
            // 
            this.textBoxAccel.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)));
            this.textBoxAccel.Location = new System.Drawing.Point(144, 340);
            this.textBoxAccel.Name = "textBoxAccel";
            this.textBoxAccel.Size = new System.Drawing.Size(35, 20);
            this.textBoxAccel.TabIndex = 50;
            this.textBoxAccel.Text = "1";
            this.textBoxAccel.TextChanged += new System.EventHandler(this.textBoxAccel_TextChanged);
            // 
            // button6
            // 
            this.button6.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.button6.BackColor = System.Drawing.Color.Red;
            this.button6.Font = new System.Drawing.Font("Microsoft Sans Serif", 14.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.button6.Location = new System.Drawing.Point(6, 19);
            this.button6.Name = "button6";
            this.button6.RightToLeft = System.Windows.Forms.RightToLeft.No;
            this.button6.Size = new System.Drawing.Size(310, 85);
            this.button6.TabIndex = 58;
            this.button6.Text = "Stop";
            this.button6.UseVisualStyleBackColor = false;
            this.button6.Click += new System.EventHandler(this.Button6_Click);
            // 
            // groupBox4
            // 
            this.groupBox4.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.groupBox4.Controls.Add(this.hScrollBarAccel);
            this.groupBox4.Location = new System.Drawing.Point(6, 346);
            this.groupBox4.Name = "groupBox4";
            this.groupBox4.Size = new System.Drawing.Size(310, 53);
            this.groupBox4.TabIndex = 59;
            this.groupBox4.TabStop = false;
            this.groupBox4.Text = "Acceleration [0, 10]";
            // 
            // hScrollBarAccel
            // 
            this.hScrollBarAccel.AllowDrop = true;
            this.hScrollBarAccel.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.hScrollBarAccel.LargeChange = 1;
            this.hScrollBarAccel.Location = new System.Drawing.Point(3, 15);
            this.hScrollBarAccel.Maximum = 10;
            this.hScrollBarAccel.Minimum = 1;
            this.hScrollBarAccel.Name = "hScrollBarAccel";
            this.hScrollBarAccel.Size = new System.Drawing.Size(304, 42);
            this.hScrollBarAccel.TabIndex = 58;
            this.hScrollBarAccel.Value = 1;
            this.hScrollBarAccel.Scroll += new System.Windows.Forms.ScrollEventHandler(this.hScrollBar1_Scroll);
            // 
            // textBoxSpeed
            // 
            this.textBoxSpeed.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)));
            this.textBoxSpeed.Location = new System.Drawing.Point(144, 281);
            this.textBoxSpeed.Name = "textBoxSpeed";
            this.textBoxSpeed.Size = new System.Drawing.Size(35, 20);
            this.textBoxSpeed.TabIndex = 50;
            this.textBoxSpeed.Text = "0";
            this.textBoxSpeed.TextChanged += new System.EventHandler(this.TextBoxYaw_TextChanged);
            // 
            // button3
            // 
            this.button3.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.button3.BackColor = System.Drawing.Color.DeepSkyBlue;
            this.button3.Font = new System.Drawing.Font("Microsoft Sans Serif", 14.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.button3.Location = new System.Drawing.Point(161, 169);
            this.button3.Name = "button3";
            this.button3.Size = new System.Drawing.Size(153, 53);
            this.button3.TabIndex = 60;
            this.button3.Text = "Break OFF";
            this.button3.TextImageRelation = System.Windows.Forms.TextImageRelation.TextBeforeImage;
            this.button3.UseVisualStyleBackColor = false;
            this.button3.Click += new System.EventHandler(this.button3_Click_1);
            // 
            // button2
            // 
            this.button2.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.button2.BackColor = System.Drawing.Color.RoyalBlue;
            this.button2.Font = new System.Drawing.Font("Microsoft Sans Serif", 14.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.button2.Location = new System.Drawing.Point(6, 169);
            this.button2.Name = "button2";
            this.button2.Size = new System.Drawing.Size(158, 53);
            this.button2.TabIndex = 59;
            this.button2.Text = "Break ON";
            this.button2.TextImageRelation = System.Windows.Forms.TextImageRelation.TextBeforeImage;
            this.button2.UseVisualStyleBackColor = false;
            this.button2.Click += new System.EventHandler(this.button2_Click_1);
            // 
            // MovesGroupBox
            // 
            this.MovesGroupBox.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.MovesGroupBox.Controls.Add(this.hScrollBarSpeed);
            this.MovesGroupBox.Location = new System.Drawing.Point(6, 287);
            this.MovesGroupBox.Name = "MovesGroupBox";
            this.MovesGroupBox.Size = new System.Drawing.Size(310, 53);
            this.MovesGroupBox.TabIndex = 51;
            this.MovesGroupBox.TabStop = false;
            this.MovesGroupBox.Text = "Speed [-400, 400]";
            // 
            // hScrollBarSpeed
            // 
            this.hScrollBarSpeed.AllowDrop = true;
            this.hScrollBarSpeed.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.hScrollBarSpeed.LargeChange = 1;
            this.hScrollBarSpeed.Location = new System.Drawing.Point(3, 15);
            this.hScrollBarSpeed.Maximum = 400;
            this.hScrollBarSpeed.Minimum = -400;
            this.hScrollBarSpeed.Name = "hScrollBarSpeed";
            this.hScrollBarSpeed.Size = new System.Drawing.Size(304, 42);
            this.hScrollBarSpeed.TabIndex = 58;
            this.hScrollBarSpeed.Value = -400;
            this.hScrollBarSpeed.Scroll += new System.Windows.Forms.ScrollEventHandler(this.HScrollBarYaw_Scroll);
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(525, 609);
            this.Controls.Add(this.groupBox2);
            this.Controls.Add(this.groupBox1);
            this.Controls.Add(this.groupBoxCommunication);
            this.Controls.Add(this.textBoxConsole);
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Name = "MainForm";
            this.StartPosition = System.Windows.Forms.FormStartPosition.Manual;
            this.Text = "Measurement arm";
            this.Load += new System.EventHandler(this.MainForm_Load);
            this.groupBoxCommunication.ResumeLayout(false);
            this.groupBox1.ResumeLayout(false);
            this.groupBox1.PerformLayout();
            this.groupBox3.ResumeLayout(false);
            this.groupBox3.PerformLayout();
            this.groupBox2.ResumeLayout(false);
            this.groupBox2.PerformLayout();
            this.groupBox4.ResumeLayout(false);
            this.MovesGroupBox.ResumeLayout(false);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private SimpleSerialPort.SimpleSerialPort simpleSerialPort;
        private System.Windows.Forms.Button buttonFlyCommand;
        private System.Windows.Forms.GroupBox groupBoxCommunication;
        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.GroupBox groupBox2;
        private GroupBox MovesGroupBox;
        private HScrollBar hScrollBarSpeed;
        public TextBox textBoxSpeed;
        private Button button6;
        private GroupBox groupBox3;
        private Button StatusLed;
        private Button PPSLed;
        private Button ENCLed;
        private Button HallLed;
        private Label label11;
        private Label label10;
        private Label label9;
        private Label label8;
        private Button button1;
        public TextBox textBoxNMEA;
        private Label label7;
        private Label label6;
        private Label label5;
        public TextBox textBoxConsole;
        public TextBox textBox4;
        public TextBox textBox2;
        public TextBox textBoxArmSpeed;
        private Label label4;
        private Label label3;
        private Label label2;
        private Label label1;
        public TextBox textBox3;
        private Button button3;
        private Button button2;
        private GroupBox groupBox4;
        private HScrollBar hScrollBarAccel;
        public TextBox textBoxAccel;
        private Button buttonRestartSynchro;
        private Label label12;
    }
}

