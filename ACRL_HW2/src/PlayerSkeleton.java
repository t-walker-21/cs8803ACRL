import java.util.*;
import java.util.concurrent.DelayQueue;
import java.awt.event.WindowEvent;
import java.io.*;
import java.net.SocketException;
import java.net.UnknownHostException;



public class PlayerSkeleton extends client { 
	//implement this function to have a working system
		public int pickMove(State s, int[][] legalMoves) throws SocketException, UnknownHostException, IOException {
		//Random generator = new Random();
		//int randomIndex = generator.nextInt(legalMoves.length);
		//System.out.println(stateToString(s));
		//String strState = stateToString(s);
		int action = recvFromPython();
		
		//System.out.println(" move chosen --> " + action);
		return action;
	}

	public int boardMaxHeight(State s)
	{
		int max = 0;
		for (int i = 0;i < s.getField().length;i++)
		{
			for (int j = 0;j < s.getField()[0].length;j++)
			{
				//System.out.println(s.getField()[i][j]);
				if (s.getField()[i][j] != 0) //record row where this occured
				{
					max = i;
				}

			}
		}
		return max;
	}

	public PlayerSkeleton() throws SocketException, UnknownHostException, IOException
	{}

	public String stateToString(State s) //takes in board state and converts to string
	{
		String str = "";

		for (int i = 0;i < s.getField().length;i++)
		{
			for (int j = 0;j < s.getField()[0].length;j++)
			{
				//System.out.println(s.getField()[i][j]);
				if (s.getField()[i][j] != 0)
				{
					str += "1";
				}

				else
				{
					str += "0";
				}

			}
		}
		//System.out.println(str.length());
		return str;
	}

	
	public static void main(String[] args) throws SocketException, UnknownHostException,IOException {
		PlayerSkeleton p = new PlayerSkeleton();
		State s;

		while (true){
			s = new State();
			TFrame t = new TFrame(s);
			int linesCleared = 0;
			String reward;
			String done = "false";
			int maxHeight = 0;

		while(!s.hasLost()) {
			int action = p.pickMove(s,s.legalMoves());
			s.makeMove(action);
			reward = "0";

			if (p.boardMaxHeight(s) - maxHeight > 0 && maxHeight != 0)
			{
				reward = "-1";
			}
			maxHeight = p.boardMaxHeight(s);

			if (linesCleared != s.getRowsCleared())
			{
				reward = "5";
				linesCleared = s.getRowsCleared();
			}
			else if(s.hasLost())
			{
				reward = "-3";
				done = "true";
			}
			
			//System.out.println("Your reward is: " + reward);
			String nxt_state = p.stateToString(s);

			//rendering env
			s.draw();
			s.drawNext(0,0);
			//rendering env

			//send next_state,reward,and done back to python
			p.sendToPython(nxt_state);
			p.sendToPython(reward);
			p.sendToPython(done);
		}
		System.out.println("agent cleared: " + linesCleared + " lines!");
		
		
		}
		
	}
}