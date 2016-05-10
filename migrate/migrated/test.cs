class Program
{
    static void Main()
    {
        Person person1 = new Person("Leopold", 6);
        Console.WriteLine("person1 Name = {0} Age = {1}", person1.Name, person1.Age);

        // Declare  new person, assign person1 to it.
        Person person2 = person1;

        //Change the name of person2, and person1 also changes.
        person2.setName("Molly");
/*Необходимо изменить имя метода. Старое имя: setNewAge, новое имя: setAge*/
        person2.setAge(16);

        Console.WriteLine("person2 Name = {0} Age = {1}", person2.Name, person2.Age);
        Console.WriteLine("person1 Name = {0} Age = {1}", person1.Name, person1.Age);

        // Keep the console open in debug mode.
        Console.WriteLine("Press any key to exit.");
        Console.ReadKey();

    }
}