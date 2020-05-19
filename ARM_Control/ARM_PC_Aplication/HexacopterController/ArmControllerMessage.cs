using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;

namespace Controller
{
    internal static class FlightControllerMessage
    {
        public static byte[] CreateMessage(char commandId, byte[] speed)
        {
            List<byte> result = new List<byte>();

            result.Add(Convert.ToByte(commandId));
            for (int i = 0; i < speed.Length; i++)
            {
                result.Add(Convert.ToByte(speed[i]));
            }
            return result.ToArray();
        }

        public static byte[] CreateMessage(char commandId, byte address, byte[] data, Int16 lenght)
        {
            List<byte> result = new List<byte>();
            //Encoding.ASCII.GetBytes(command);
            
            // add header
            result.Add(Convert.ToByte(commandId));
            // add data
            data = data.Take(lenght).ToArray();
            result.AddRange(data);
            
            // add footer
            result.AddRange(GetCrcBytes(result.ToArray()));
            result.Add(Convert.ToByte('\r'));

            return result.ToArray();
        }

        public static byte[] CreateMyMessage(byte address, char commandId, byte[] data)
        {
            List<byte> result = new List<byte>();

            //Encoding.ASCII.GetBytes(command);

            // add header
            result.Add(Convert.ToByte('#'));
            result.Add((byte)(Convert.ToByte('a') +  address));
            result.Add(Convert.ToByte(commandId));

            // add data
            result.AddRange(Encode64(data));

            // add footer
            result.AddRange(GetCrcBytes(result.ToArray()));
            result.Add(Convert.ToByte('\r'));

            return result.ToArray();
        }

        public static void ParseMessage(byte[] message, out char commandId, out byte address, out byte[] data)
        {
            Debug.Assert(message.Length >= 6);

            // header
            // '#' == message[0]
            commandId = Convert.ToChar(message[1]);
            address = (byte)(message[2] - Convert.ToByte('a'));

            // data
            data = Decode64(message, 3, message.Length - 6);

            // footer
            // CRC1 == message[message.Length - 3]
            // CRC2 == message[message.Length - 2]
            // '\r' == message[message.Length - 1]
        }

        public static byte[] Encode64(byte[] data)
        {
            List<byte> encodedData = new List<byte>();

            byte a,b,c;
            int index = 0;
            byte k = Convert.ToByte('=');

            while (index < data.Length)
            {
                if (index < data.Length) a = data[index++]; else a = 0;
                if (index < data.Length) b = data[index++]; else b = 0;
                if (index < data.Length) c = data[index++]; else c = 0;

                encodedData.Add((byte)(k + (a >> 2)));
                encodedData.Add((byte)(k + (((a & 0x03) << 4) | ((b & 0xf0) >> 4))));
                encodedData.Add((byte)(k + (((b & 0x0f) << 2) | ((c & 0xc0) >> 6))));
                encodedData.Add((byte)(k + ( c & 0x3f)));
            }

            return encodedData.ToArray();
        }

        
        public static byte[] Decode64(byte[] data, int startIndex, int count)
        {
            // data should be in chunks of 4 right?
            Debug.Assert(count % 4 == 0);

            List<byte> decodedData = new List<byte>();

            byte k = Convert.ToByte('=');
            byte a,b,c,d;
            byte x,y,z;
            int index = startIndex;

            while (index <= count-4)
            {
                a = (byte)(data[index++] - k);
                b = (byte)(data[index++] - k);
                c = (byte)(data[index++] - k);
                d = (byte)(data[index++] - k);

                x = (byte)((a << 2) | (b >> 4));
                y = (byte)(((b & 0x0f) << 4) | (c >> 2));
                z = (byte)(((c & 0x03) << 6) | d);

                decodedData.Add(x);
                decodedData.Add(y);
                decodedData.Add(z);
            }

            return decodedData.ToArray();
        }


        // cyclic redundancy check (CRC) or polynomial code checksum used to verify message
        // it is an insecure hash function designed to detect accidental changes to raw computer data (wikipedia)
        private static byte[] GetCrcBytes(byte[] data)
        {
            byte[] crcBytes = new byte[2];

            uint tmpCrc = 0;
            for(int i = 0; i < data.Length ;i++)
            {
                tmpCrc += data[i];
            }
            tmpCrc %= 4096;
            crcBytes[0] = (byte)(Convert.ToByte('=') + tmpCrc / 64);
            crcBytes[1] = (byte)(Convert.ToByte('=') + tmpCrc % 64);

            return crcBytes;
        }
    }
}
