---
title: 2 Creating and Destroying Objects
---

THIS chapter concerns creating and destroying objects: 

* when and how to *create* them
* when and how to *avoid creating* them
* how to ensure they are *destroyed in a timely manner*
* how to manage any *cleanup* actions that must precede their destruction

### Item 1: Consider static factory methods instead of constructors

The traditional way to obtain an instance is to provide a public constructor. Also a public *static factory method*(静态工厂方法), which returns an instance of the class:

```Java
// translates a Boolean primitive value 
// into a Boolean object reference
public static Boolean valueOf(boolean b) { 
    return b ? Boolean.TRUE : Boolean.FALSE; 
}
```

The static factory method has no direct equivalent in Design Patterns.

#### advantage

* have names: a static factory can describe the object being returned. 
    * e.g. `BigInteger(int, int, Random)`, which returns a `BigInteger` that is probably prime, would have been better expressed as `BigInteger.probablePrime`.
    * A class can have only a single constructor with a given signature. To get around this restriction, Programmers provide two constructors whose parameter lists differ only in the order of their parameter types. Easy to make mistake. 
    * In cases where a class seems to require multiple constructors with the same signature, replace the constructors with static factory methods and carefully chosen names to highlight their differences.
* NOT required to create a new object each time they’re invoked.
    * allow immutable classes to use pre-constructed instances
    * or to cache instances as they’re constructed, and dispense them repeatedly to avoid creating unnecessary duplicate objects
    * e.g `:::Java Boolean.valueOf(boolean)` method *never* creates an object.
* return an object of any subtype of their return type.
* the class of the returned object can vary from call to call as a function of the input parameters.
* the class of the returned object need not exist when the class containing the method is written.

#### Disadvantage

* The main limitations that classes without public or protected constructors cannot be subclassed.
* They are hard for programmers to find. -> adhering to common naming conventions(from, of, valueOf, getInstance, newInstance)



### Item 2: Consider a builder when faced with many constructor parameters

Static factories and constructors share a limitation: they do not scale well to large number of optional parameters.

!!! example "Nutrition"
    
    ```java
    NutritionFacts cocaCola = new NutritionFacts(240, 8, 100, 0, 35, 27);
    ```
    The telescoping constructor pattern works, but it is hard to write client code when there are many parameters, and harder still to read it. 




Instead of making the desired object directly, the client calls a constructor (or static factory) with all of the required parameters and *gets a builder object*. Then the client calls setter-like methods on the builder object to set each optional parameter of interest. Finally, the client *calls a parameterless build method* to generate the object, which is typically immutable.


```java
public class NutritionFacts {

    private final int servingSize;
    private final int servings;
    private final int calories;
    private final int fat;
    private final int sodium;
    private final int carbohydrate;

    public static class Builder {
        // Required parameters
        private final int servingSize;
        private final int servings;

        // Optional parameters - initialized to default values
        private int calories = 0;
        private int fat = 0;
        private int sodium = 0;
        private int carbohydrate = 0;

        public Builder(int servingSize, int servings) {
            this.servingSize = servingSize;
            this.servings = servings;
        }

        public Builder calories(int val) {
            calories = val;
            return this;
        }

        public Builder fat(int val) {
            fat = val;
            return this;
        }

        public Builder sodium(int val) {
            sodium = val;
            return this;
        }

        public Builder carbohydrate(int val) {
            carbohydrate = val;
            return this;
        }

        public NutritionFacts build() {
            return new NutritionFacts(this);
        }

    }

    private NutritionFacts(Builder builder) {
        servingSize = builder.servingSize;
        servings = builder.servings;
        calories = builder.calories;
        fat = builder.fat;
        sodium = builder.sodium;
        carbohydrate = builder.carbohydrate;
    }

    public static void main(String[] args) {
       NutritionFacts cocaCola = new NutritionFacts
               .Builder(240, 8)
               .calories(100).sodium(35).carbohydrate(27).build();
    }

}
```


### Item 3: Enforce the singleton property with a private constructor or an enum type
### Item 4: Enforce noninstantiability with a private constructor
### Item 5: Prefer dependency injection to hardwiring resources
### Item 6: Avoid creating unnecessary objects 
### Item 7: Eliminate obsolete object references
### Item 8: Avoid finalizers and cleaners 
### Item 9: Prefer try-with-resources to try-finally

Historically, a `try-finally` statement was the best way to guarantee that a resource would be closed properly. However, problem still exists:

* `close()` will fail if read/write fails due to a failure in the underlying physical device.

Using `try-with-resources` statement, a resource will automatically close resources. To be useable, a resource must implement the <C>AutoClosable</C> interface, which consists of a single `void`-returning `close` method.

```java
public interface AutoCloseable {
    void close() throws Exception;
}
```

Examples using try-with-resources, for Single resource and multiple resources:

```java tab="Single Resource"
// try-with-resources - the the best way to close resources! 
static String firstLineOfFile(String path) throws IOException {
    try (BufferedReader br = new BufferedReader( new FileReader(path))) {
        return br.readLine();
    }
}
```

```java tab="Multiple Resource"
// try-with-resources on multiple resources - short and sweet 
static void copy(String src, String dst) throws IOException { 
    try (InputStream in = new FileInputStream(src); 
            OutputStream out = new FileOutputStream(dst)) { 
        byte[] buf = new byte[BUFFER_SIZE]; 
        int n; 
        while ((n = in.read(buf)) >= 0) 
            out.write(buf, 0, n); 
    }
}
```

**Always use `try`-with-resources in preference to `try-finally` when working with resources that must be closed.**.