#include <beanbackend/greeter.h>                        // for Greeter
#include <beanbackend/http_handlers/greeter_handler.h>  // for GreeterHandler

#include <string>                                      // for string
#include <userver/server/http/http_request.hpp>        // for HttpRequest
#include <userver/server/request/request_context.hpp>  // for RequestContext
namespace greeter
{
  std::string GreeterHandler::HandleRequestThrow(
      const userver::server::http::HttpRequest &request,
      userver::server::request::RequestContext & /* request_context */) const
  {
    const Greeter greeter{ request.GetArg("lang") };
    return greeter.greet();
  }

};  // namespace greeter
