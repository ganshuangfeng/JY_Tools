using System;
using System.IO;
using System.Text;
using System.Windows.Forms;
using System.Security.Cryptography;

namespace WindowsFormsApp1
{

    public partial class Form1 : Form
    {

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }


        public static byte [] EncryptBase(byte[] Text, string sKey,bool is_decrypt = false)
        {
            SymmetricAlgorithm oSym = DES.Create();

            System.IO.MemoryStream oMem = new System.IO.MemoryStream();

            byte[] AKey = Encoding.UTF8.GetBytes(sKey);

            byte[] AIV = Encoding.UTF8.GetBytes(sKey);

            CryptoStream oStream = new CryptoStream(oMem, is_decrypt ? oSym.CreateDecryptor(AKey, AIV) : oSym.CreateEncryptor(AKey, AIV), CryptoStreamMode.Write);

            byte[] AInput = Text;

            oStream.Write(AInput, 0, AInput.Length);

            oStream.Close();

            //return Encoding.UTF8.GetString(oMem.ToArray());
            return oMem.ToArray();
        }

        public static string Encrypt(string sText,string sKey = "LfeJHJ3f")
        {
            return "$vmap$" + Convert.ToBase64String(EncryptBase(Encoding.UTF8.GetBytes(sText), sKey));
        }
        public static string Decrypt(string sText, string sKey = "LfeJHJ3f")
        {
            if (sText.Length < 6)
                return null;
            if (sText.Substring(0, 6) != "$vmap$")
                return null;

            return Encoding.UTF8.GetString(EncryptBase(Convert.FromBase64String(sText.Substring(6)), sKey,true));
        }

        private void button1_Click(object sender, EventArgs e)
        {
            string text = System.IO.File.ReadAllText(textBox1.Text);

            // 加密
            string outtext = Encrypt(text);

            File.WriteAllText(textBox2.Text, outtext);
        }
        
        private void button2_Click(object sender, EventArgs e)
        {
            string text = System.IO.File.ReadAllText(textBox1.Text);

            // 解密
            string outtext = Decrypt(text);

            if (outtext != null)
                File.WriteAllText(textBox2.Text, outtext);
        }
    }
}
