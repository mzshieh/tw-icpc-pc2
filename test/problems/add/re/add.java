import java.io.*;
import java.lang.*;
import java.util.*;

class add{
	public static void main(String args[]) throws Exception
	{
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		for(String line = br.readLine(); line != null; line = br.readLine())
		{
			StringTokenizer st = new StringTokenizer(line);
			long x = Long.parseLong(st.nextToken());
			long y = Long.parseLong(st.nextToken());
			System.out.println(x+y);
		}
		System.exit(1);
	}
}
