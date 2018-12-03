### **Hadoop: The Definitive Guide 6 - Developing a MapReduce Application**

### 1 The Configuration API

Components in Hadoop are configured using Hadoop’s own configuration API. An instance of the <C>org.apache.hadoop.conf.Configuration</C> represents a collection of configuration properties and their values.

<C>Configuration</C>s read their properties from  XML files, which have a simple structure for defining name-value pairs.


!!! note
    XML(E**x**tensible **M**arkup **L**anguage, 可扩展标记语言), is a markup language that defines a set of rules for encoding documents in a format that is both human-readable and machine-readable. 
    
#### Combining Resources

When more than one resource is used to define a <C>Configuration</C>, properties added later override the earlier definitions. However, properties that are marked as <C>final</C> cannot be overridden in later definitions.

```Java
Configuration conf = new Configuration();
conf.addResource("configuration-1.xml");
conf.addResource("configuration-2.xml");
assertThat(conf.getInt("size", 0), is(12));
assertThat(conf.get("weight"), is("heavy"));
```

```xml fct_label="configuration-1.xml"
<?xml version="1.0"?> 
<configuration>
    <property> 
        <name>color</name> 
        <value>yellow</value> 
        <description>Color</description> 
    </property>

    <property> 
        <name>size</name> 
        <value>10</value> 
        <description>Size</description> 
    </property>

    <property> 
        <name>weight</name> 
        <value>heavy</value> 
        <final>true</final> 
        <description>Weight</description> 
    </property>

    <property> 
        <name>size-weight</name> 
        <value>${size},${weight}</value> 
        <description>Size and weight</description> 
    </property> 
</configuration>
```

```xml fct_label="configuration-2.xml"
<?xml version="1.0"?> 
<configuration>
    <property> 
        <name>size</name> 
        <value>12</value> 
    </property>

    <property> 
        <name>weight</name> 
        <value>light</value> 
    </property> 
</configuration>
```

#### Variable Expansion

Configuration properties can be defined in terms of other properties, or system properties. For example, the property <C>size-weight</C> in `configuration-1.xml` file is defined as ` $text{size}$, ${weight}$`.

### 2 Setting Up the Development Environment

The first step is to create a project so you can build MapReduce programs and run them in local (standalone) mode from the command line or within your IDE. 

Using the Maven POM to manage your project is an easy way to start. Specifically, for building MapReduce jobs, you only need to have the <C>hadoop-client</C> dependency, which contains all the Hadoop client-side classes needed to interact with HDFS and MapReduce. For running unit tests, use <C>junit</C>, and for writing MapReduce tests, use <C>mrunit</C>. The <C>hadoop-minicluster</C> library contains the “mini-” clusters that are useful for testing with Hadoop clusters running in a single JVM.

#### Managing Configuration

When developing Hadoop applications, it is common to switch between running the application locally and running it on a cluster.

One way to accommodate these variations is to have different versions of Hadoop configuration files and use them with the <C>-conf</C> command-line switch.

For example, the following command shows a directory listing on the HDFS server running in pseudodistributed mode on localhost:

```
$ hadoop fs -conf conf/hadoop-localhost.xml -ls
```


Another way of managing configuration settings is to copy the etc/hadoop directory from your Hadoop installation to another location, place the `*-site.xml` configuration files there (with appropriate settings), and set the <C>HADOOP_CONF_DIR </C>environment variable to the alternative location. The main advantage of this approach is that you don’t need to specify <C>-conf</C> for every command.

#### GenericOptionsParser, Tool, and ToolRunner

It’s more convenient to implement the <C>Tool</C> interface and run your application with the <C>ToolRunner</C>. <C>ToolRunner</C> uses <C>GenericOptionsParser</C> internally, which interprets common Hadoop command-line options and sets them on a <C>Configuration</C> object for your application to use as desired.

```Java
//  A tool interface that supports handling of generic command-line options.
public interface Tool extends Configurable { 
    int run(String [] args) throws Exception; 
}
```

Detailed examples, are "Application to find the maximum temperature"[[code](ch6/#running-a-job-in-a-local-job-runner)], "MapReduce program to find the maximum temperature, creating Avro output"[[code](ch12/#avro-mapreduce)].


### 3 Writing a Unit Test with MRUnit

<C>MRUnit</C> is a testing library that makes it easy to pass known inputs to a mapper or a reducer and check that the outputs are as expected.  However, MRUnit is **DEPRECATED**!!!



### 4 Running Locally on Test Data


#### Running a Job in a Local Job Runner

Using the <C>Tool</C> interface, it’s easy to write a driver to run our MapReduce job for finding the maximum temperature by year.

```Java
public class MaxTemperatureDriver extends Configured implements Tool {

  @Override
  public int run(String[] args) throws Exception {
    if (args.length != 2) {
      System.err.printf("Usage: %s [generic options] <input> <output>\n",
          getClass().getSimpleName());
      ToolRunner.printGenericCommandUsage(System.err);
      return -1;
    }
    
    Job job = new Job(getConf(), "Max temperature");
    job.setJarByClass(getClass());

    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    
    job.setMapperClass(MaxTemperatureMapper.class);
    job.setCombinerClass(MaxTemperatureReducer.class);
    job.setReducerClass(MaxTemperatureReducer.class);

    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(IntWritable.class);
    
    return job.waitForCompletion(true) ? 0 : 1;
  }
  
  public static void main(String[] args) throws Exception {
    int exitCode = ToolRunner.run(new MaxTemperatureDriver(), args);
    System.exit(exitCode);
  }
}
```

From the command line, we can run the driver by typing:




#### Testing the Driver
### 5 Running on a Cluster
### 6 Tuning a Job
### 7 MapReduce Workflows