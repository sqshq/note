### **Lab 1: javac, java, git**

Add the skeleton remote repository, and pull from the skeleton remote in order to get the starter code for lab 1.

```bash
$ git remote add skeleton https://github.com/Berkeley-CS61B/skeleton-sp18.git
$ git pull skeleton master
```

#### Leap Year

In the lab1 folder, you should see a file called `LeapYear.java`. This program is supposed to test whether or not a given year is a Leap Year. The user will give a year as a command line parameter (examples given below), and then print out whether or not that year is a leap year, e.g.

```bash
$ java LeapYear 2000 
2000 is a leap year.
$ java LeapYear 1999 
1999 is not a leap year. 
$ java LeapYear 2004 
2004 is a leap year.
$ java LeapYear 2100 
2100 is not a leap year.
```

A leap year is either:

* divisible by 400 or
* divisible by 4 and not by 100.


Requirement:

* Make sure to provide a description of the method as a comment. Your description should be contained by /** and */ (JavaDocs). 
* Use the @source tag any time you receive significant help on a project.

Some Java tips:

* The % operator implements remainder.
* The != operator compares two values for inequality.
* When one of the arguments of the + operator is a String, the arguments are concatenated as Strings.

```Java
/** Class that determines whether or not a year is a leap year.
 *  @author zhenhua wang
 */
public class LeapYear {

    /** Calls isLeapYear to print correct statement.
     *  @param  year to be analyzed
     */
    private static void checkLeapYear(int year) {
        if (isLeapYear(year)) {
            System.out.printf("%d is a leap year.\n", year);
        } else {
            System.out.printf("%d is not a leap year.\n", year);
        }
    }

    /** Check if the year  is a leap year
     * @param year int year
     */
    private static boolean isLeapYear(int year) {
        if (year%400 == 0)
            return true;
        else if ((year%4==0) && (year %100 !=0))
            return true;
        return false;
    }




    /** Must be provided an integer as a command line argument ARGS.
     * @param args int year
     */
    public static void main(String[] args) {
        if (args.length < 1) {
            System.out.println("Please enter command line arguments.");
            System.out.println("e.g. java Year 2000");
        }
        for (int i = 0; i < args.length; i++) {
            try {
                int year = Integer.parseInt(args[i]);
                checkLeapYear(year);
            } catch (NumberFormatException e) {
                System.out.printf("%s is not a valid number.\n", args[i]);
            }
        }
    }
}
```