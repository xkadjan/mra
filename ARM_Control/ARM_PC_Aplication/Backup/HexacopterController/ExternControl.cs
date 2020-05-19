using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Diagnostics;

namespace HexacopterController
{
    class ExternControl
    {
        byte digital0;
        byte digital1;
        byte remoteVisualization;
        sbyte pitch;
        sbyte yaw;
        sbyte roll;
        byte throttle;
        sbyte high;       		 // affects the pressure sensor according to the MoteCtrl project comments
        byte unused;             // free unused byte
        byte frameConfirmation;  // confimation
        byte config; 		 // set to 1 to signal new command

        public ExternControl(byte[] data)
        {
            Bytes = data;
        }

        public ExternControl(sbyte yaw, sbyte pitch, sbyte roll, byte throttle)
        {
            digital0 = 0;
            digital1 = 0;
            remoteVisualization = 0;
            this.pitch = pitch;
            this.roll = roll;
            this.yaw = yaw;
            this.throttle = throttle;
            high = 0;
            unused = 0;
            frameConfirmation = 0;
            config = 1;
        }

        public sbyte Pitch
        {
            get { return pitch; }
            set { pitch = value; }
        }

        public sbyte Roll
        {
            get { return roll; }
            set { roll = value; }
        }

        public sbyte Yaw
        {
            get { return yaw; }
            set { yaw = value; }
        }

        public byte Throttle
        {
            get { return throttle; }
            set { throttle = value; }
        }

        public byte[] Bytes
        {
            get
            {
                byte[] data = new byte[11];

                data[0] = digital0;
                data[1] = digital1;
                data[2] = remoteVisualization;
                data[3] = (byte)pitch;
                data[4] = (byte)roll;
                data[5] = (byte)yaw;
                data[6] = throttle;
                data[7] = (byte)high;
                data[8] = unused;
                data[9] = frameConfirmation;
                data[10] = config;

                return data;
            }
            set
            {
                Debug.Assert(value.Length >= 11);

                digital0 = value[0];
                digital1 = value[1];
                remoteVisualization = value[2];
                pitch = (sbyte)value[3];
                roll = (sbyte)value[4];
                yaw = (sbyte)value[5];
                throttle = value[6];
                high = (sbyte)value[7];
                unused = value[8];
                frameConfirmation = value[9];
                config = value[10];
            }
        }
    }
}
