import java.net.*;

import javax.imageio.IIOException;

import java.io.*;


public class client {
    private DatagramSocket socket;
    private DatagramSocket socket2;
    private InetAddress address;
 
    private byte[] buf;
 
    public client() throws SocketException, UnknownHostException {
        socket = new DatagramSocket();
        address = InetAddress.getByName("localhost");

        socket2 = new DatagramSocket(5006);
    }
 
    public void sendToPython(String msg) throws IOException {
        buf = msg.getBytes();
        DatagramPacket packet = new DatagramPacket(buf, buf.length, address, 5005);
        socket.send(packet);
    }

    public int recvFromPython() throws IOException
    {
        DatagramPacket packet;
        packet = new DatagramPacket(new byte[10], (new byte[10]).length);
        //System.out.println("waiting for response");
        socket2.receive(packet);
        String received = new String(packet.getData(), 0, packet.getLength());
        return Integer.parseInt(received);
    }
 
    public void close() {
        socket.close();
    }
}