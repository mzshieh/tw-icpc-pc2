import java.io.*;
import java.util.*;

public class InnerClasses{

    static int n, m;
    static Map<Point, Point> pMap;
    static Map<Edge, Edge> eMap;
    static Set<Triangle> tSet;

    public static void main(String[] args){
        Scan scan = new Scan();
        int testcases = scan.nextInt();
        while(testcases-- != 0){
            n = scan.nextInt();
            m = scan.nextInt();
            pMap = new HashMap<>();
            eMap = new HashMap<>();
            tSet = new HashSet<>();
            Point first = new Point(scan.nextInt(), scan.nextInt());
            Point last = new Point(scan.nextInt(), scan.nextInt());
            for(int i=2;i<n;i++){
                Point now = new Point(scan.nextInt(), scan.nextInt());
                Triangle triangle = new Triangle(first, last, now);
                tSet.add(triangle);
                last = now;
            }
            //printTriangles();
            for(int i=0;i<m;i++){
                Point now = new Point(scan.nextInt(), scan.nextInt());
                Set<Triangle> newSet = new HashSet<>();
                for(Triangle t : tSet){
                    int det = (t.p2.y-t.p3.y) * (t.p1.x-t.p3.x) + (t.p3.x-t.p2.x) * (t.p1.y-t.p3.y);
                    int c1 = (t.p2.y-t.p3.y) * (now.x-t.p3.x) + (t.p3.x-t.p2.x) * (now.y-t.p3.y);
                    int c2 = (t.p3.y-t.p1.y) * (now.x-t.p3.x) + (t.p1.x-t.p3.x) * (now.y-t.p3.y);
                    int c3 = det - c1 - c2;
                    if(c1 < 0 || c1 > det || c2 < 0 || c2 > det || c3 < 0 || c3 > det){
                        newSet.add(t);
                        continue;
                    }
                    for(int j=0;j<3;j++){
                        t.edges[j].triangles.remove(t);
                        if(t.edges[j].triangles.isEmpty()) eMap.remove(t.edges[j]);
                    }
                    if(c1 == 0){
                        newSet.add(new Triangle(now, t.p1, t.p2));
                        newSet.add(new Triangle(now, t.p1, t.p3));
                    }else if(c2 == 0){
                        newSet.add(new Triangle(now, t.p1, t.p2));
                        newSet.add(new Triangle(now, t.p2, t.p3));
                    }else if(c3 == 0){
                        newSet.add(new Triangle(now, t.p1, t.p3));
                        newSet.add(new Triangle(now, t.p2, t.p3));
                    }else{
                        newSet.add(new Triangle(now, t.p1, t.p2));
                        newSet.add(new Triangle(now, t.p1, t.p3));
                        newSet.add(new Triangle(now, t.p2, t.p3));
                    }

                }
                tSet = newSet;
            }
            //printTriangles();
            int[][] matrix = new int[3][3];
            ArrayList<Edge> list = new ArrayList<>();
            list.addAll(eMap.keySet());
            for(int i=0;i<list.size();i++){
                //System.out.println("i = "+i);
                Edge e = list.get(i);
                Queue<Edge> queue = new ArrayDeque<>();
                queue.add(e);
                while(!queue.isEmpty()){
                    Edge now = queue.poll();
                    //System.out.println("now = "+now.p1+" <-> "+now.p2);
                    if(now.triangles.size() < 2) continue;
                    Triangle t1 = now.triangles.get(0);
                    Triangle t2 = now.triangles.get(1);
                    Point d = null;
                    if(t2.edges[0] == now) d = t2.p1; 
                    else if(t2.edges[1] == now) d = t2.p2;
                    else if(t2.edges[2] == now) d = t2.p3;
                    int selecter = determinant(t1.p1, t1.p2, t1.p3, d);
                    if(selecter <= 0) continue;
                    Point d2 = null;
                    if(t1.edges[0] == now) d2 = t1.p1; 
                    else if(t1.edges[1] == now) d2 = t1.p2;
                    else if(t1.edges[2] == now) d2 = t1.p3;
                    if((d.x-d2.x)*(d.y-now.p1.y) == (d.y-d2.y)*(d.x-now.p1.x)) continue;
                    if((d.x-d2.x)*(d.y-now.p2.y) == (d.y-d2.y)*(d.x-now.p2.x)) continue;
                    Edge newEdge = new Edge(d, d2);
                    //System.out.println("change to "+newEdge.p1+" "+newEdge.p2);
                    tSet.remove(t1);
                    tSet.remove(t2);
                    Triangle a = new Triangle(d, d2, now.p1);
                    Triangle b = new Triangle(d, d2, now.p2);
                    tSet.add(a);
                    tSet.add(b);
                    eMap.remove(now);
                    for(int j=0;j<3;j++){
                        t1.edges[j].triangles.remove(t1);
                        t2.edges[j].triangles.remove(t2);
                        Edge temp = t1.edges[j];
                        if(temp != now){
                            //if(temp.p1 == now.p1 || temp.p2 == now.p1) temp.triangles.add(a);
                            //else temp.triangles.add(b);
                            queue.add(temp);
                        }
                        temp = t2.edges[j];
                        if(temp != now){
                            //if(temp.p1 == now.p1 || temp.p2 == now.p1) temp.triangles.add(a);
                            //else temp.triangles.add(b);
                            queue.add(temp);
                        }
                    }
                }
            }
            double result = 100;
            //printTriangles();
            for(Triangle t : tSet){
                result = Math.min(result, getAngle(t.p1, t.p3, t.p2));
                result = Math.min(result, getAngle(t.p2, t.p1, t.p3));
                result = Math.min(result, getAngle(t.p3, t.p2, t.p1));
            }
            result = result * 180 / Math.PI;
            System.out.printf("%.10f\n", result);
        }
    }

    static void printTriangles(){
        System.out.println("================");
        for(Triangle t : tSet){
            System.out.println(t.p1+" "+t.p2+" "+t.p3);
        }
        System.out.println("================");
    }

    static int determinant(Point a, Point b, Point c, Point d){
        int[][] matrix = new int[3][3];
        int result = 0;
        matrix[0][0] = a.x - d.x; matrix[0][1] = a.y - d.y; matrix[0][2] = a.x*a.x + a.y*a.y - d.x*d.x - d.y*d.y; 
        matrix[1][0] = b.x - d.x; matrix[1][1] = b.y - d.y; matrix[1][2] = b.x*b.x + b.y*b.y - d.x*d.x - d.y*d.y; 
        matrix[2][0] = c.x - d.x; matrix[2][1] = c.y - d.y; matrix[2][2] = c.x*c.x + c.y*c.y - d.x*d.x - d.y*d.y;
        result += matrix[0][0]*(matrix[1][1]*matrix[2][2] - matrix[1][2]*matrix[2][1]);
        result -= matrix[1][0]*(matrix[0][1]*matrix[2][2] - matrix[0][2]*matrix[2][1]);
        result += matrix[2][0]*(matrix[0][1]*matrix[1][2] - matrix[0][2]*matrix[1][1]);
        //System.out.println("Test "+a+" "+b+" "+c+" "+d+" : "+result);
        return result;
    }

    static double getAngle(Point a, Point b, Point c){
        Point v1 = new Point(b.x-a.x, b.y-a.y);
        Point v2 = new Point(c.x-a.x, c.y-a.y);
        double product = v1.x*v2.x + v1.y*v2.y;
        double cos = product / Math.hypot(v1.x, v1.y) / Math.hypot(v2.x, v2.y);
        return Math.acos(cos);
    }

    static class Point implements Comparable<Point>{

        int x, y;

        Point(int x, int y){
            this.x = x;
            this.y = y;
        }

        @Override
            public int hashCode(){
                return ((x+10000)<<15) + (y+10000);
            }

        @Override
            public boolean equals(Object o){
                if(o == null) return false;
                if(o instanceof Point){
                    Point rhs = (Point)o;
                    if(x==rhs.x && y==rhs.y) return true;
                }
                return false;
            }

        @Override
            public int compareTo(Point rhs){
                if(x == rhs.x) return y - rhs.y;
                return x - rhs.x;
            }

        @Override
            public String toString(){
                return "("+x+", "+y+")";
            }

    }

    static class Edge{

        Point p1, p2;
        ArrayList<Triangle> triangles;

        Edge(Point p1, Point p2){
            p1 = pMap.getOrDefault(p1, p1);
            p2 = pMap.getOrDefault(p2, p2);
            if(p1.compareTo(p2) < 0){
                this.p1 = p1;
                this.p2 = p2;
            }else{
                this.p1 = p2;
                this.p2 = p1;
            }
            triangles = new ArrayList<>();
        }

        @Override
            public int hashCode(){
                return p1.hashCode() ^ p2.hashCode();
            }

        @Override
            public boolean equals(Object o){
                if(o == null) return false;
                if(o instanceof Edge){
                    Edge rhs = (Edge)o;
                    if(p1.equals(rhs.p1) && p2.equals(rhs.p2)) return true;
                    if(p1.equals(rhs.p2) && p2.equals(rhs.p1)) return true;
                }
                return false;
            }

    }

    static class Triangle{

        Point p1, p2, p3;
        Edge[] edges;

        Triangle(Point p1, Point p2, Point p3){
            p1 = pMap.getOrDefault(p1, p1);
            p2 = pMap.getOrDefault(p2, p2);
            p3 = pMap.getOrDefault(p3, p3);
            Point temp;
            if(p2.compareTo(p1) < 0 && p2.compareTo(p3) < 0){
                temp = p2;
                p2 = p1;
                p1 = temp;
            }else if(p3.compareTo(p1) < 0 && p3.compareTo(p2) < 0){
                temp = p3;
                p3 = p1;
                p1 = temp; 
            }
            if((p2.x-p1.x) * (p3.y-p2.y) - (p2.y-p1.y) * (p3.x-p2.x) < 0){
                temp = p3;
                p3 = p2;
                p2 = temp;
            }
            this.p1 = p1;
            this.p2 = p2;
            this.p3 = p3;
            edges = new Edge[3];
            Edge token = new Edge(p2, p3);
            edges[0] = eMap.getOrDefault(token, token);
            if(edges[0] == token) eMap.put(token, token);
            edges[0].triangles.add(this);
            token = new Edge(p1, p3);
            edges[1] = eMap.getOrDefault(token, token);
            if(edges[1] == token) eMap.put(token, token);
            edges[1].triangles.add(this);
            token = new Edge(p1, p2);
            edges[2] = eMap.getOrDefault(token, token);
            if(edges[2] == token) eMap.put(token, token);
            edges[2].triangles.add(this);
        }

        @Override
            public int hashCode(){
                return p1.hashCode() ^ p2.hashCode() ^ p3.hashCode();
            }

        @Override
            public boolean equals(Object o){
                if(o == null) return false;
                if(o instanceof Triangle){
                    Triangle rhs = (Triangle)o;
                    if(p1.equals(rhs.p1) && p2.equals(rhs.p2) && p3.equals(rhs.p3)) return true;
                }
                return false;
            }

    }

}

class Scan{

    BufferedReader buffer;
    StringTokenizer tok;

    Scan(){
        buffer = new BufferedReader(new InputStreamReader(System.in));
    }

    boolean hasNext(){
        while(tok==null || !tok.hasMoreElements()){
            try{
                tok = new StringTokenizer(buffer.readLine());
            }catch(Exception e){
                return false;
            }
        }
        return true;
    }

    String next(){
        if(hasNext()) return tok.nextToken();
        return null;
    }

    int nextInt(){
        return Integer.parseInt(next());
    }

}
