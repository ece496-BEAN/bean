#include <beanbackend/greeter.h>  // for LanguageCode, Greeter
#include <beanbackend/version.h>  // for GREETER_VERSION

#include <cxxopts.hpp>    // for value, OptionAdder, Options, OptionValue
#include <iostream>       // for basic_ostream, operator<<, endl, cout
#include <memory>         // for shared_ptr, __shared_ptr_access
#include <string>         // for allocator, char_traits, operator<<, hash
#include <unordered_map>  // for unordered_map, operator==, _Node_const_...
#include <utility>        // for pair

auto main(int argc, char **argv) -> int
{
  try
  {
    const std::unordered_map<std::string, greeter::LanguageCode> languages{
      { "en", greeter::LanguageCode::EN },
      { "de", greeter::LanguageCode::DE },
      { "es", greeter::LanguageCode::ES },
      { "fr", greeter::LanguageCode::FR },
    };

    cxxopts::Options options(*argv, "A program to welcome the world!");

    std::string language;
    std::string name;

    // clang-format off
  options.add_options()
    ("h,help", "Show help")
    ("v,version", "Print the current version number")
    ("n,name", "Name to greet", cxxopts::value(name)->default_value("World"))
    ("l,lang", "Language code to use", cxxopts::value(language)->default_value("en"))
  ;
    // clang-format on

    auto result = options.parse(argc, argv);

    if (result["help"].as<bool>())
    {
      std::cout << options.help() << '\n';
      return 0;
    }

    if (result["version"].as<bool>())
    {
      std::cout << "Greeter, version " << GREETER_VERSION << '\n';
      return 0;
    }

    auto langIt = languages.find(language);
    if (langIt == languages.end())
    {
      std::cerr << "unknown language code: " << language << '\n';
      return 1;
    }

    const greeter::Greeter greeter(name);
    std::cout << greeter.greet(langIt->second) << '\n';

    return 0;
  }
  catch (...)
  {
    std::cerr << "exception\n";
  }
}
