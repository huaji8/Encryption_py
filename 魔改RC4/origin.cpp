
#include <iostream>
#include <stdio.h>  
#include <string.h>  

template<class T> inline void
swap(T& i, T& j)
{
    T tmp = i;
    i = j;
    j = tmp;
}
class RC4
{
public:
    void SetKey(char* K, int keylen);
    void Transform(char* output, const char* data, int len);
private:
    unsigned char S[256];
};

//初始化S盒
void RC4::SetKey(char* K, int keylen)
{
    for (int i = 0; i < 256; i++)
    {
        S[i] = i;
    }
    int j = 0;
    for (int i = 0; i < 256; i++)
    {
        j = (j + S[i] + K[i % keylen]) % 256;
        swap(S[i], S[j]);
    }
}
//生成密钥流
void RC4::Transform(char* output, const char* data, int len)
{
    int i = 0, j = 0;
    unsigned char key;
    for (int k = 0; k < len; k++)
    {
        i = (i + 1) % 256;
        j = (j + S[i]) % 256;
        swap(S[i], S[j]);
        key = S[(S[i] + S[j]) % 256];
        output[k] = key ^ data[k];
    }
}

int main()
{
    char data[256] = "wednesday is shit";
    char output[256] = "";
    printf("明文:%s\n", data);
    char K[] = "iamevilcalf";
    int keylen = sizeof(K);
    RC4 rc4encrypt, rc4decrypt;
    rc4encrypt.SetKey(K, keylen);
    rc4decrypt.SetKey(K, keylen);
    rc4encrypt.Transform(output, data, strlen(data));
    printf("密文: %s\n", output);
    rc4decrypt.Transform(output, output, strlen(data));
    printf("解密后明文: %s\n", output);
    return 0;
}