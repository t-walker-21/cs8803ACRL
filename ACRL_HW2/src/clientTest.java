import java.io.IOException;
import java.net.SocketException;
import java.net.UnknownHostException;

public class clientTest
{
    public static void main(String[] args) throws SocketException, UnknownHostException, IOException
    {
        client c = new client();
        System.out.println("hello");
        while (true){

        System.out.println(c.sendToPython("hello There"));
        }
    }


}